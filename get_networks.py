## generate networks:
### networks by act & scene
### an overall network
## store networks in file/DB for quick access

import json
import re

def create_scenes_dict(this_text):
    """
    Extract the individual scenes from an act and create a dictionary.
    
    Args:
        this_text - str; the text of an act.
    
    Returns:
        scenes_dict - dict; keys are the titles of scenes (e.g. 'SCENE I') and values are lists of lists where the zeroth element is a character's name and the first element is their line as a str.
    """
    this_text_clean = this_text.split('\n\n')
    this_text_clean = [i.strip() for i in this_text_clean if len(i)>0] # list of str
    
    temp = []
    scene_indices = []
    for i in this_text_clean:
        found = re.split(r'\b([A-Z]+\s?[A-Z]+?)\b', i) # if split re creates a split the first element in resulting list will be empty, we're relying on that in the conditional below
        if not found[0]:
            found[-1] = found[-1].replace('.\n',' ').replace('\n',' ').lstrip()
            temp.append(found[1:])
    
#     for i,e in enumerate(temp):
#         if e and (((e[0].startswith('SCENE')) or (e[0].startswith('Scene')))):
#             print(i,e)
            
    scene_indices = [i for i, e in enumerate(temp) if e and ((e[0].startswith('SCENE')) or (e[0].startswith('Scene')))]
    scene_indices.append(len(temp))
    
    these_scenes = []
    these_bodies = []
    for j in scene_indices:
        try:
            these_chars = temp[j:scene_indices[scene_indices.index(j)+1]]
            this_scene = these_chars.pop(0)
            
            these_scenes.append(this_scene[0].upper())
            these_bodies.append(these_chars)
        except Exception as e:
            pass

    scenes_dict = dict(zip(these_scenes, these_bodies))
    
    return scenes_dict

def create_acts_dict(acts):
    """
    Extract the individual acts and create a dictionary where keys are the titles of acts and values are the text of the scenes.
    
    Args:
        acts - str; the main text of the play.
        
    Returns:
        acts_dict - dict; dict of dicts where keys are the titles of acts (e.g. 'ACT II') and values are dicts of scenes. 
    """
    these_acts = []
    these_bodies = []
    while acts:
        this_item = acts.pop(0)
        if len(this_item)<100:
            these_acts.append(this_item)
        else:
            scenes_dict = create_scenes_dict(this_item)
            these_bodies.append(scenes_dict)
    assert not acts, 'Check acts var. Still contains content.'
    assert (len(these_acts)==5) and (len(these_bodies)==5), 'Verify lists generation. Play should have five acts.'
    
    acts_dict = dict(zip(these_acts,these_bodies))
        
    return acts_dict
    

def get_chars_acts(data):
    """
    Extract the main content from the text; the acts and scenes.
    
    Args:
        data - str; the text of the play. 
        
    Returns:
        characters - str; the initial list of characters & general setting of the play.
        acts - str; the main text of the play; the acts and scenes.
    """
    _, body, _ = re.split(r'\*{3}[^\*]+THIS PROJECT GUTENBERG EBOOK[^\*]+\*{3}', data) # find body of text, discard header & footer
    assert len(body) >= 0.8*len(data), 'Verify split of body, header, & footer. May have bad split.'
    
    _, body = re.split(r'\bDramatis\sPerson.', body) # find body of text, discard table of contents
    characters, *acts = re.split(r'\b(ACT\s\w+)', body) # characters contains the initial listing of characters & general setting; acts contains the main text of the play
    assert sum([len(i) for i in acts]) >= 0.95*len(body), 'Verify split of acts. May have bad split.'
    
    return characters, acts
    

def get_data(play):
    """
    Open file and load contents of play.
    
    Args:
        this_play - str; the play to retrieve.
        
    Returns:
        data - str; the contents of the file.
    """
    this_file = open(SHAKESPEARE[play]['path'], 'r')
    data = this_file.read()
    this_file.close()
    
    return data
    
    
if __name__ == '__main__':
    
    SHAKESPEARE = {
    'romeo':{
        'url':'https://www.gutenberg.org/files/1513/1513-0.txt',
        'path': 'data/romeo.txt',
        'node_color': '#ca9ae1',
        'title': 'Romeo & Juliet'
    },
    'othello':{
        'url':'https://www.gutenberg.org/files/1531/1531-0.txt',
        'path': 'data/othello.txt',
        'node_color':'#9999ff',
        'title': 'Othello, the Moor of Venice'
    },
    'hamlet':{
        'url':'https://www.gutenberg.org/files/1524/1524-0.txt',
        'path': 'data/hamlet.txt',
        'node_color': '#ffbc66',
        'title': 'Hamlet'
    },
    'caesar':{
        'url': 'https://www.gutenberg.org/files/1522/1522-0.txt',
        'path': 'data/caesar.txt',
        'node_color': '#9AB1E1',
        'title': 'Julius Caesar'
    },
    'macbeth':{
        'url': 'https://www.gutenberg.org/files/1533/1533-0.txt',
        'path': 'data/macbeth.txt',
        'node_color': '#FF9999',
        'title': 'Macbeth'
    },
    'midsummer':{
        'url': 'https://www.gutenberg.org/files/1514/1514-0.txt',
        'path': 'data/midsummer.txt',
        'node_color': '#e1a79a',
        'title': 'A Midsummer Night’s Dream'
    }
}
    
    all_dicts = {}    
    for entry in SHAKESPEARE.keys():
        this_data = get_data(entry)
        chars, acts = get_chars_acts(this_data)
        full_dict = create_acts_dict(acts) # contains a dict of dicts with characters & lines by turn
        all_dicts[entry] = full_dict
        
        with open(f'data/{entry}_acts_scenes.json', 'w') as outfile:
            json.dump(full_dict, outfile) 
        
    with open('data/shakespeare_acts_scenes.json', 'w') as outfile:
        json.dump(all_dicts, outfile)        
