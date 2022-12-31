def create_graf():
    graf = {}
    graf['you'] = ['ilia', 'mikasa', 'denis', 'kate']
    graf['ilia'] = ['alex', 'ann', 'dima', 'valet']
    graf['mikasa'] = ['levi', 'jhan', 'ervin']
    graf['denis'] = ['artem', 'alex', 'ann', 'nika', 'pasha']
    graf['kate'] = ['ralf', 'li']
    graf['alex'] = ['eran', 'naruto']
    graf['ann'] = ['sasuke', 'sergei', 'prokop']
    graf['prokop'] = ['nuruto', 'levi']
    graf ['dima'] = []
    graf ['valet'] = []
    graf ['levi'] = []
    graf ['jhan'] = []
    graf ['ervin'] = []
    graf ['artem'] = []
    graf ['nika'] = []
    graf ['pasha'] = []
    graf ['prokop'] = []
    graf ['ralf'] = []
    graf ['li'] = []
    graf ['eran'] = []
    graf ['naruto'] = []
    graf ['sasuke'] = []
    graf ['sergei'] = []

    return graf


from collections import deque

def search_in_weight(graf):
    search_list = deque()
    search_list +=graf['you']
    searched = []
    step = 1

    while search_list:
        person = search_list.popleft()
        print(person + ': step ' + str(step))

        if not person in searched:
            if person_is_hokage(person):
                print(person + ' is a hokage')
                return True
            else:
                search_list +=graf[person]
                searched.append(person)
        step +=1
    return False

def person_is_hokage(person):
    return person[0] == 'n'

if __name__ == '__main__':
    search_in_weight(create_graf())