from split_and_merge import split_and_merge_dataset
from blank_and_hanja_and_concat import blank_and_hanja_and_concat
import json, csv

# Training data
unanswerable_path = './dataset/Training/TL_unanswerable/TL_unanswerable.json'
span_path = './dataset/Training/TL_span_extraction/TL_span_extraction.json'
how_path = './dataset/Training/TL_span_extraction_how/TL_span_extraction_how.json'

# Validation data
v_unanswerable_path = './dataset/Validation/VL_unanswerable/VL_unanswerable.json'
v_span_path = './dataset/Validation/VL_span_extraction/VL_span_extraction.json'
v_how_path = './dataset/Validation/VL_span_extraction_how/VL_span_extraction_how.json'

n = 1.5
f_num = {1: 18, 1.5: 12, 3: 8, 5: 4}

split_and_merge_dataset(unanswerable_path, span_path, how_path, n=n, train_data=True)
split_and_merge_dataset(v_unanswerable_path, v_span_path, v_how_path, n=n, train_data=False)

with open(f'./dataset/training_{f_num[n]}m.json', 'r', encoding='utf-8') as f:
    train = json.load(f)
with open(f'./dataset/validation_{f_num[n]}m.json', 'r', encoding='utf-8') as f:
    dev = json.load(f)

concat_w = []
with open('concat_words.tsv', 'r', encoding='utf-8') as f:
    tr = csv.reader(f, delimiter='\t')
    for _ in tr:
        concat_w.append(_)
concat_w = sorted(concat_w, key=lambda x: len(x[1]), reverse=True)

for x in [train, dev]:
    for data in x['data']:
        p = data['paragraphs'][0]
        p['context'] = blank_and_hanja_and_concat(p['context'])
        for qas in p['qas']:
            if qas['is_impossible'] == False:
                qas['answers'][0]['text'] = blank_and_hanja_and_concat(qas['answers'][0]['text'], concat_w)
                qas['answers'][0]['answer_start'] = p['context'].find(qas['answers'][0]['text'], concat_w)


with open(f'./dataset/pre_training_{f_num[n]}m.json', 'w') as f:
    json.dump(train, f, ensure_ascii=False, indent=2)
with open(f'./dataset/pre_validation_{f_num[n]}m.json', 'w') as f:
    json.dump(dev, f, ensure_ascii=False, indent=2)
