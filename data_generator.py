import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import random
import os
import cv2
from tqdm import tqdm 
from img_utils import *

def build_sample(colors, img_size, object_size):

    # choose two random colors
    color1 = ()
    color2 = ()
    while color1 == color2:
        color1 = colors[random.randint(0,5)]
        color2 = colors[random.randint(0,5)]

    color1_id = colors.index(color1)
    color2_id = colors.index(color2)
    
    # get quesiton type and coordinates for each condition
    positions = [([25,25],[65,25]),([160,25],[200,25]), ([25,175],[65,175]), ([160,175],[200,175])]
    question_type = [0,1,2,3]

    zipped_list = list(zip(positions, question_type))
    random.shuffle(zipped_list)
    positions, question_type = zip(*zipped_list)

    objects = []

    img = np.ones((img_size,img_size,3)) * 255

    img, objects = draw_sCsS(img, positions, color1, color1_id, objects, size = object_size)
    img, objects = draw_sCdS(img, positions, color2, color2_id, objects, size = object_size)
    img, objects = draw_dCsS(img, positions, color1, color2, color1_id, color2_id, objects, size = object_size)
    img, objects = draw_dCdS(img, positions, color1, color2, color1_id, color2_id, objects, size = object_size)

    img = (img).astype('uint8')
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    return (img, objects, list(question_type))

def build_question(question_type):


    # question_type = [0,1,2,3] # shuffle positions with question_type
    # random.shuffle(question_type)

    order_type = [0,0,1,1]
    random.shuffle(order_type)

    raw_questions = list(zip(question_type, order_type))

    question_texts = []
    programs = []
    answers = []
    question_code_strings = ['sCsS', 'sCdS', 'dCsS', 'dCdS']
    ans_dict = {i:j for i,j in list(zip(question_code_strings, question_type))}

    question_text_types = [['the same color', 'the same shape', 'sCsS'],['the same color','a different shape', 'sCdS'],\
            ['a different color','the same shape', 'dCsS'], ['a different color','a different shape','dCdS']]

    for q_type,o_type in raw_questions:

        order = [0,1] if o_type == 0 else [1,0]
        
        question_texts.append(f'Which pair is {question_text_types[q_type][order[0]]} and {question_text_types[q_type][order[1]]}?')

        # Add to the programs
        text_type1 = question_text_types[q_type][order[0]]
        text_type2 = question_text_types[q_type][order[1]]
        answers.append(ans_dict[question_text_types[q_type][2]])

        program = f'generate pair <nxt>\
    filter {text_type1.split()[-2:][0]}_{text_type1.split()[-2:][1]} <nxt>\
    filter {text_type2.split()[-2:][0]}_{text_type2.split()[-2:][1]} <nxt>\
    query pair'
        
        programs.append(program)
    
    return (question_texts, programs, answers)

def make_directories(data_dir, img_dir):
    try:
        os.makedirs(data_dir)
    except:
        pass
    
    try:
        os.makedirs(img_dir)
    except:
        pass

def build_dataset(num_samples, img_size, colors, object_size, data_dir, prefix='train'):
    
    samples = [build_sample(colors, img_size, object_size) for _ in range(num_samples)]

        
    # Init dataframes
    img_det_df = pd.DataFrame(columns=['filename', 'width', 'height', 'class', 'xmin', 'ymin', 'xmax', 'ymax'])
    que2prog_df = pd.DataFrame(columns=['filename', 'answer', 'query_text', 'program_text']) 
    
    img_dir = os.path.join(data_dir, 'images')
    shape_map = {'r': 'rectangle', 'c': 'circle'}

    # generate data and image directories
    make_directories(data_dir, img_dir)

    for i, sample in enumerate(tqdm(samples)):
        img, objects, question_type = sample

        #save img
        filename = f'{i}.jpg'
        img_path = os.path.join(img_dir, filename)
        cv2.imwrite(img_path, img)

        # Append the image data to dataframes
        for obj in objects:
            color_id, shape, bbox = obj[0], shape_map[obj[2]], obj[3]
            
            img_det_df = img_det_df.append({'filename': filename, 
                                            'width': img_size, 
                                            'height': img_size, 
                                            'class': 'obj', 
                                            'xmin': bbox[0], 'ymin': bbox[1],
                                            'xmax': bbox[2], 'ymax': bbox[3]}, ignore_index=True)
            
        # Do the same for the text data
        question_texts, programs, answers = build_question(question_type)

        for que, prog, ans in list(zip(question_texts, programs, answers)):
            que2prog_df = que2prog_df.append({'filename': filename, 
                                    'answer': ans, 
                                    'query_text': que, 
                                    'program_text': prog}, ignore_index=True)

    img_det_df.to_csv(os.path.join(data_dir, f'{prefix}_img_det.csv'), index=False)
    que2prog_df.to_csv(os.path.join(data_dir, f'{prefix}_que2prog.csv'), index=False)