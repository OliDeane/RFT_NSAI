import pandas as pd

def generate_pair(scene):
    # creat seaprate columns fro x and yposition
    scene['x_pos'] = [pos[0] for pos in list(scene['position'])]
    scene['y_pos'] = [pos[1] for pos in list(scene['position'])]

    #sort by x and y position
    scene = scene.sort_values(["y_pos", 'x_pos'], ascending = (True, True))

    # remove the extra columns and reset the index of the dataframe
    del scene['x_pos']
    del scene['y_pos']
    scene = scene.reset_index(drop=True)

    # Add a pair_ids colum
    pair_ids = list(range(int(len(scene)/2)))*2
    pair_ids.sort() 
    scene['pair_id'] = pair_ids
    
    return scene

def relate(scene, attribute, relation):
    result = []
    for id in scene['pair_id']:
        pair = scene[scene['pair_id']==id]
        pair=pair.reset_index(drop=True)

        if relation == 'different':
            if pair[attribute][0] != pair[attribute][1] and id not in result:
                result.append(id)

        elif relation == 'same':
            if pair[attribute][0] == pair[attribute][1] and id not in result:
                result.append(id)

    return scene[scene['pair_id'].isin(result)]


def filter_different_shape(scene):
    return relate(scene, attribute = 'shape', relation = 'different')

def filter_different_color(scene):
    return relate(scene, attribute = 'color', relation = 'different')

def filter_same_shape(scene):
    return relate(scene, attribute = 'shape', relation = 'same')

def filter_same_color(scene):
    return relate(scene, attribute = 'color', relation = 'same')

def query_pair(scene):
    return list(scene['pair_id'])[0]
        