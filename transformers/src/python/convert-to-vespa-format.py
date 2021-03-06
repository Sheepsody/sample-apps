#! /usr/bin/env python3

import os
import io
import sys
import csv
import json

from transformers import AutoTokenizer


data_dir = sys.argv[1]
doc_type = sys.argv[2]
fields = sys.argv[3].split(",")
model_name = sys.argv[4]
sequence_length = 128

sample_offset_file = os.path.join(data_dir, "test-docs-offset.tsv")
docs_file = os.path.join(data_dir, "docs.tsv")
out_file = os.path.join(data_dir, "vespa.json")

tokenizer = AutoTokenizer.from_pretrained(model_name)


def load_document_offsets():
    docoffset = {}
    with io.open(sample_offset_file, 'r', encoding='utf8') as f:
        tsvreader = csv.reader(f, delimiter="\t")
        for [docid, offset] in tsvreader:
            docoffset[docid] = int(offset)
    return docoffset


def tokenize(doc):
    title = doc["fields"]["title"]
    body = doc["fields"]["body"]
    tokens = tokenizer.encode_plus(title + body, add_special_tokens=False, max_length=sequence_length, pad_to_max_length=True)
    return tokens["input_ids"]


def main():
    document_offsets = load_document_offsets()

    docs = 0
    with io.open(docs_file, "r", encoding="utf-8") as f, open(out_file, "w") as out:
        out.write("[\n")
        for docid in document_offsets.keys():
            f.seek(document_offsets[docid])
            line = f.readline()
            line = line.strip()
            content = line.split("\t")

            found_docid = content[0]
            if found_docid != docid:
                continue  # dataset has some wrong lookup values
            if len(content) != len(fields):
                continue  # missing fields

            if docs > 0:
                out.write(",\n")
            docs += 1

            doc = { "put" : f"id:{doc_type}:{doc_type}::{docid}", "fields" : {} }
            for i, field in enumerate(fields):
                doc["fields"][field] = content[i]
            doc["fields"]["tokens"] = { "values": tokenize(doc) }
            json.dump(doc, out)

        out.write("\n]\n")


if __name__ == "__main__":
    main()


