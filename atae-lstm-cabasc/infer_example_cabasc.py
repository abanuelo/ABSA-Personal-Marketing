# -*- coding: utf-8 -*-
# file: infer.py
# author: songyouwei <youwei0314@gmail.com>
# Copyright (C) 2019. All Rights Reserved.

import torch
import torch.nn.functional as F
import argparse

from data_utils import build_tokenizer, build_embedding_matrix
from models import IAN, MemNet, ATAE_LSTM, AOA, Cabasc


class Inferer:
    """A simple inference example"""
    def __init__(self, opt, path_global):
        self.opt = opt
        self.tokenizer = build_tokenizer(
            fnames=[opt.dataset_file['train'], opt.dataset_file['test']],
            max_seq_len=opt.max_seq_len,
            dat_fname='{0}_tokenizer.dat'.format(opt.dataset))
     
        p = path_global + '{0}_{1}_embedding_matrix.dat'.format(str(opt.embed_dim), opt.dataset)
        #print("THIS IS THE P THAT I AM TRYING TO PRINT YO: ", p)
        embedding_matrix = build_embedding_matrix(
            word2idx=self.tokenizer.word2idx,
            embed_dim=opt.embed_dim,
            dat_fname=p)
        self.model = opt.model_class(embedding_matrix, opt)
        #print('loading model {0} ...'.format(opt.model_name))
        self.model.load_state_dict(torch.load(opt.state_dict_path))
        self.model = self.model.to(opt.device)
        # switch model to evaluation mode
        self.model.eval()
        torch.autograd.set_grad_enabled(False)

    def evaluate(self, raw_texts, keyword):
        #Need to split to right and left of the keyword sequence
        sentence = raw_texts[0]
        index_keyword = int(sentence.index(keyword))
        left_side = sentence[:index_keyword]
        right_side = sentence[index_keyword + len(keyword):]

        context_seqs = [self.tokenizer.text_to_sequence(raw_text.lower().strip()) for raw_text in raw_texts]
        aspect_seqs = [self.tokenizer.text_to_sequence(keyword)] * len(raw_texts) #can put 'null' as a catch all statement
        left_seqs = [self.tokenizer.text_to_sequence(left_side)]
        right_seqs = [self.tokenizer.text_to_sequence(right_side)]
        context_indices = torch.tensor(context_seqs, dtype=torch.int64).to(self.opt.device)
        aspect_indices = torch.tensor(aspect_seqs, dtype=torch.int64).to(self.opt.device)
        left_indices = torch.tensor(left_seqs, dtype=torch.int64).to(self.opt.device)
        right_indices = torch.tensor(right_seqs, dtype=torch.int64).to(self.opt.device)


        # print(aspect_seqs)
        # print(context_seqs)
        t_inputs = [context_indices, aspect_indices, left_indices, right_indices]
        t_outputs = self.model(t_inputs)

        t_probs = F.softmax(t_outputs, dim=-1).cpu().numpy()
        return t_probs

def main(sentence, keyword, path): 

    model_classes = {
        'cabasc': Cabasc,
        'atae_lstm': ATAE_LSTM,
        'ian': IAN,
        'memnet': MemNet,
        'aoa': AOA,
    }
    # set your trained models here
    model_state_dict_paths = {
        'cabasc': path + 'state_dict/cabasc_car_val_acc0.8133',
        # 'ian': 'state_dict/ian_restaurant_acc0.7911',
        # 'memnet': 'state_dict/memnet_restaurant_acc0.7911',
        # 'aoa': 'state_dict/aoa_restaurant_acc0.8063',
    }
    class Option(object): pass
    opt = Option()
    opt.model_name = 'cabasc'
    opt.model_class = model_classes[opt.model_name]
    opt.dataset = 'car'
    train_path = ''
    test_path = ''
    if len(path) > 0:
        train_path = path + 'datasets/semeval14/Car_Train.xml.seg'
        test_path = path + 'datasets/semeval14/Car_Test_Gold.xml.seg'
    else:
        train_path = './datasets/semeval14/Car_Train.xml.seg'
        test_path = './datasets/semeval14/Car_Test_Gold.xml.seg'
    opt.dataset_file = {
        'train': train_path,
        'test': test_path
    }
    opt.state_dict_path = model_state_dict_paths[opt.model_name]
    opt.embed_dim = 300
    opt.hidden_dim = 300
    opt.max_seq_len = 80
    opt.polarities_dim = 4
    opt.hops = 3
    opt.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    inf = Inferer(opt, path)
    t_probs = inf.evaluate([sentence], keyword)
    #print(t_probs.argmax(axis=-1) - 1)
    return (t_probs.argmax(axis=-1) - 1)


if __name__ == '__main__':
    result = main(sentence, keyword, path) #path can either be blank '' or have the root directory info
