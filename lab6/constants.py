import re

root_dir = '/home/marcin/Desktop/SemestrVIII/PJN'
year = "2018"
json_data_dir = f"{root_dir}/data/json"
tagging_file = 'tagging-2018.data'


patterns = {
    re.compile('A?C.*') : 'civil',
    re.compile('A?U.*') : 'insurance',
    re.compile('A?K.*') : 'criminal', 
    re.compile('G.*') :  'economic',
    re.compile('A?P.*'): 'work', 
    re.compile('R.*'): 'family', 
    re.compile('W.*') : 'violations', 
    re.compile('Am.*'): 'competition'  ,
    re.compile('.*'): 'other' 
    }



common_words = ['w', 'z', 'na', 'i', 'do',
 'nie', 'o', 'k', 'r', 'że',
 'art', 'dnia', 'się', 'od', 'a',
 'przez', 'sąd', 'roku', 'pracy', 'za']

common_tagged_words =['w:prep', 'z:prep', 'na:prep', 
                      'i:conj', 'do:prep', 'nie:qub', 'dzień:subst',
                     'on:ppron3', 'o:prep', 'rok:brev', 'sąd:subst',
                     'że:comp', 'koło:brev', 'praca:subst', 'ten:adj',
                     'artykuł:brev', 'się:qub', 'od:prep', 'rok:subst', 'przez:prep']

