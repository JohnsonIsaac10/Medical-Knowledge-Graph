
import jieba
import re

"""处理病因数据"""
def process_cause():
    write_cause_file = open('cause_baike.txt', mode='w')
    #
    file_cause = open('MedicalKG_cause.txt')
    #
    temp_list = []
    for line in file_cause.readlines():
        new_line = line.replace('\n', '')
        new_line = re.split('、|；|，', new_line)
        for cause in new_line:
            temp_list.append(cause)

        print(new_line)

    temp_list = set(temp_list)
    for cause in temp_list:
        if cause == '疾病':
            continue
        else:
            write_cause_file.write(cause+'\n')


"""处理症状数据"""
def process_symptom():
    write_symptom_file = open('symptom_baike.txt', mode='w')
    #
    file_symptom = open('MedicalKG_symptom.txt')
    #
    temp_list = []
    for line in file_symptom.readlines():
        new_line = line.replace('\n', '')
        new_line = re.split('、|；|，', new_line)
        for symptom in new_line:
            temp_list.append(symptom)

        print(new_line)

    temp_list = set(temp_list)
    for symptom in temp_list:
        write_symptom_file.write(symptom + '\n')


"""停用词处理"""
def process_stopwords():
    file_symptom = open('symptom_baike.txt')
    file_cause = open('cause_baike.txt')

    stop_words = open('StopWords.txt')

    write_symtom_stopwords = open('symptom_stopwords.txt', mode='w')
    write_cause_stopwords = open('cause_stopwords.txt', mode='w')

    stopwords = stop_words.read().split('\n')

    for line in file_symptom.readlines():
        line_seg = jieba.lcut(line)
        print(line_seg)
        out = ''
        for word in line_seg:
            if word not in stopwords:
                if word != '\t':
                    out += word
        print(out)
        write_symtom_stopwords.write(out)

    for line in file_cause.readlines():
        line_seg = jieba.lcut(line)
        print(line_seg)
        out = ''
        for word in line_seg:
            if word not in stopwords:
                if word != '\t':
                    out += word
        print(out)
        write_cause_stopwords.write(out)