# create file to:
## pull down & process text for plays
## generate networks:
### networks by act & scene
### an overall network
## store networks in file/DB for quick access

import re

def get_scenes(this_text):
    """
    """
    found = re.findall(r'\b([A-Z]+\s?[A-Z]+?)\b', this_text)
    
    scene_indices = [i for i, e in enumerate(found) if ((e.startswith('SCENE')) or (e.startswith('Scene')))]
    scene_indices.append(len(found))
    
    these_scenes = []
    these_bodies = []
    for j in scene_indices:
        try:
          these_chars = found[j:scene_indices[scene_indices.index(j)+1]]
          this_scene = these_chars.pop(0)

          these_scenes.append(this_scene)
          these_bodies.append(these_chars)
        except:
          pass

    scenes_dict = dict(zip(these_scenes, these_bodies))
    
    return scenes_dict

def create_acts_dict(acts):
    """
    Extract the individual acts and create a dictionary where keys are the titles of acts and the values are the text of the scenes.
    
    Args:
        acts - str; the main text of the play
        
    Returns:
        acts_dict - dict; dict where keys are the titles of acts and the values are the text of the scenes
    """
    these_acts = []
    these_bodies = []
    while acts:
      this_item = acts.pop(0)
      if len(this_item)<100:
        these_acts.append(this_item)
      else:
        scenes_dict = get_scenes(this_item)
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
        characters - str; the initial list of characters & general setting of the play 
        acts - str; the main text of the play; the acts and scenes
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
        data - str; the contents of the file
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
    }
}
    
    for entry in SHAKESPEARE.keys():
        this_data = get_data(entry)
        chars, acts = get_chars_acts(this_data)
        acts_dict = create_acts_dict(acts) # acts_dict is 
        
        print(entry, acts_dict.values())
                