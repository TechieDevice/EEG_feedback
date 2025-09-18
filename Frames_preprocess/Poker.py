import random
from poker import Card
from poker import Suit

def sort_merge(list1, list2):
    return sorted(list1 + list2, reverse=True)


def suits_ct(hand):
    ct_s = [0, 0, 0, 0]
    for i in range(len(hand)):
        ct_s[hand[i]%4]+=1
    return(ct_s)

def rank_ct(hand):
    ct_r = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    for i in range(len(hand)):
        ct_r[hand[i]//4]+=1
    return(ct_r)



def create_deck():
    deck = [i for i in range(0,52)]
    random.shuffle(deck)
    return(deck)

def print_cards(a):
    for i in range(len(a)):
        print_card(a[i])
    print('')

def points(hand):
    points = 0
    for i in range(5):
            points += hand[i]//4*13**(4-i)
    return(points)


def pop_cards(a, n):
    b = a[0:n]
    a = a[n:]
    return(a,b)

def print_card(a):
    rank = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
    suite = name = ['♠', '♣', '♦', '♥']
    print(rank[a//4], suite[a%4], end = " ", sep ="")

def full_test(hand_f):
        ranks = rank_ct(hand_f)
        suits = suits_ct(hand_f)
        #print(hand_f)
        #print(ranks)
        #print(suits)
        flag = -1
        flag, points, b_hand = test_flash(hand_f, ranks, suits)
        if flag == -1:
            flag, points, b_hand = test_street(hand_f, ranks)
        if (flag == -1)|(flag<7):
            flag1, points1, b_hand1 = test_kare(hand_f, ranks)
            if flag1>flag:
                flag = flag1
                points = points1
                b_hand = b_hand1
        if (flag == -1)|(flag<6):
            flag1, points1, b_hand1 = test_set(hand_f, ranks)
            if flag1>flag:
                flag = flag1
                points = points1
                b_hand = b_hand1
        #if flag == -1:
        #    flag1, points1, b_hand1 = test_pairs(hand_f, ranks)

        if flag == -1:
            flag, points, b_hand = test_high(hand_f, ranks)
        print(flag, points, end = ' ')
        print_cards(b_hand)



def test_high(a, r):
    if max(r) == 1:
        b_hand = a[:5]
        return(0, points(b_hand), b_hand)
    else:
        return(-1, 0, [])


def test_kare(a, r):
    b_hand=[]
    if max(r) == 4:
        rank = a.index(max(a))
        if a[0]//4 == rank:
            b_hand.append(a[:5])
        else:
            b_hand.append(rank*4, rank*4+1, rank*4+2, rank*4+3, a[0])
        return(7, points(b_hand), b_hand)
    else:
        return(-1, 0, [])


def test_set(a, r):
    b_hand=[]
    r = r[::-1]

    if max(r) == 3:
        rank = r.index(max(r))
        rank1 = -1
        r[rank]=0
        for i in range(13):
            if r[i]>=2:
                rank1 = i
                break
        for i in range(len(a)):
            if a[i]//4 == rank:
                b_hand.append(a[i])
                a[i] = -1
        cta = 0
        if rank1!=-1:
            for i in range(len(a)):
                if a[i]//4 == rank1:
                    b_hand.append(a[i])
                    cta +=1
                if cta ==2:
                    flag = 6
                    break
        else:
            for i in range(len(a)):
                if a[i]!=-1:
                    b_hand.append(a[i])
                    cta +=1
                if cta ==2:
                    flag = 3
                    break
        return(flag, points(b_hand), b_hand)
    else:
        return(-1, 0, [])


def test_street(a, r):
    b_hand = []
    r.append(0)
    max_len = 0
    max_i = -1
    c_len = 0
    for i in range(len(r)):
        if r[i]==0:
            if c_len==5:
                max_i = i - 1
                break
            else:
                c_len = 0
        else:
            c_len += 1
    #print(max_len, max_i, '!!!')
    if c_len>4:
        for i in range(len(a)):
            #print('!!!', st, a[i], a)
            if a[i]//4 == max_i:
                b_hand.append(a[i])
                max_i -= 1
        return(4, points(b_hand), b_hand)
    else:
        return(-1, 0, [])

def test_flash(a, r, s):
    if max(s) >= 5:
        suit = 0
        for i in range(4):
            if s[i]>=5:
                suit = i
                break
        b_hand = []
        for i in range(len(a)):
            if a[i]%4 == suit:
                b_hand.append(a[i])
        fs, fs_points, bfs_hand = test_street(b_hand, rank_ct(b_hand))
        if b_hand == 4:
            return(8, fs_points, bfs_hand)
        else:
            #print(b_hand, len(b_hand), b_hand[len(b_hand)-5:])
            b_hand = b_hand[:5]
            return(5, points(b_hand), b_hand)
    else:
        return(-1, 0, [])



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    deck = create_deck()
    n_play = 10
    print_cards(deck)
    hands = []
    for i in range(n_play):
        deck, hand = pop_cards(deck, 2)
        hands.append(hand)
        print_cards(hand)
    deck, flop = pop_cards(deck, 3)
    deck, tern = pop_cards(deck, 1)
    deck, river = pop_cards(deck, 1)
    table = sort_merge(flop, tern)
    table = sort_merge(table, river)
    print_cards(table)
    print_cards(deck)
    hands_f = []
    for i in range(n_play):
        hand_f = sort_merge(table, hands[i])
        hands_f.append(hand_f)
        print('---------------HAND ',i,'--------------------------')
        res = full_test(hand_f)
        print_cards(hand_f)
    


    
