#!/usr/bin/env python
# coding: utf-8


import json
from copy import deepcopy
import argparse


# *************************************
# PART-1, TASK-1-2-3-4: Class InvertedIndex with methods init and query.

"""
Class InvertedIndex takes the build_inverted_index's output (from task_2). 
The function build_inverted_index returns InvertedIndex object. 
Method query takes iterable as an argument, choose common articles for all words in the query.
"""
class InvertedIndex:

    def __init__(self, word_to_docs_mapping):
        self.__index_dict = deepcopy(word_to_docs_mapping)

        
    def query(self, words):
        
        article_list = None
        
        for w in words:
            if article_list is None:
                article_list = deepcopy(self.__index_dict.get(w, set()))
            else:
                article_list &= self.__index_dict.get(w, set())    
            if not article_list:
                break
                
        return article_list # set of common article_id for all words

    
    def dump(self, filepath):
        with open(filepath, 'w', encoding='utf8') as file:   
            f_sets = lambda x: list(x) if isinstance(x, set) else x
            json.dump(self.__index_dict, file, default=f_sets)

        
    @classmethod
    def load(cls, filepath):
        with open(filepath, encoding='utf8') as file:
            json_dict = json.load(file)
        
        for key, value in json_dict.items():
            json_dict[key] = set(value)
            
        return cls(json_dict) # InvertedIndex object



"""
The function 'load_document()' takes as an argument the path to the Wikipedia dump file. 
This function returns a dictionary where the key is article_id 
and the value is the article name and its content. 
"""
def load_document(filepath):
    article_dict = {}
    
    with open(filepath, encoding = 'utf8') as file:
        for raw in file:
            article_id, article_name_content = raw.split('\t', maxsplit=1)
            article_dict[int(article_id)] = article_name_content.strip()
            
    return  article_dict # {article_id: article_name + article_content}



"""
The function 'build_inverted_index()' takes the load_document's output as a parameter 
and returns a dictionary {word: set of article_id}. 
"""
def build_inverted_index(articles):
    index_dict = {}
    
    for article_id, article_content in articles.items():
        for word in article_content.split():
            index_dict.setdefault(word, set()).add(article_id)
    
    return InvertedIndex(index_dict) # InvertedIndex object


# *************************************
# PART-2: Command Line Interface (CLI)

"""
The function constructs inverted_index and saves to disk.
"""
def CLI_construct_index(args):
    build_index_data = build_inverted_index(load_document(args.dataset))
    build_index_data.dump(args.index)



"""
The function finds common articles for words in each query from the query file.
"""
def CLI_query(args):
    index_data = InvertedIndex.load(args.index)
    
    with open(args.queries, encoding='utf8') as file:
        for raw in file:
            print(*sorted(index_data.query(raw.split())), sep=',')
    

    
parser = argparse.ArgumentParser(description = 'Building and querying inverted_index')
sub_parsers = parser.add_subparsers()

build_parser = sub_parsers.add_parser(
    'build', help = 'takes a dump as input, creates an inverted_index, and saves it to disk')

build_parser.add_argument(
    '--dataset', dest = 'dataset', required = True,
    help = 'path to dataset to build inverted_index')

build_parser.add_argument(
    '--index', dest = 'index', default = 'index-dump.json',
    help = 'path for inverted_index dump')

build_parser.set_defaults(func = CLI_construct_index)

query_parser = sub_parsers.add_parser(
    'query', help = 'find common articles for words in each query from the query-file')

query_parser.add_argument(
    '--query_file', dest = 'queries', required = True,
    help = 'path to file with collection of queries')

query_parser.add_argument(
    '--index', dest = 'index', default = 'index-dump.json', 
    help = 'path to load inverted_index')

query_parser.set_defaults(func = CLI_query)

if __name__ == '__main__':
    args = parser.parse_args()
    
    if not vars(args):
        parser.print_usage()
    else:
        args.func(args)

