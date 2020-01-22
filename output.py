import alchemy as db

def output(num):
    bits = db.db_session.query(db.Torrant.bit).limit(num).all()
    length = len(bits)
    mangent = ''
    for x in range(length):
        if x+1 == length:
            pass
        else:
            if bits[x] is not None:
                print(bits[x][0])
                mangent = mangent + bits[x][0] + '\n'
    print(mangent)

if __name__ == '__main__':
    output(80)
    