import alchemy as db

def pipeline(items):
    for item in items:
        try:
            if item['bit'] is not None:
                new_torrant = db.Torrant(
                    title=item['title'],
                    link=item['link'],
                    download=item['download'],
                    image=item['image'],
                    bit=item['bit'],
                    num=item['num'],
                    gallary=item['gallary']
                )
                print(item)
                db.db_session.add(new_torrant)
                self.link_set.add(item['download'])

        except Exception as e:
            # print(item)
            print("Failed to into database")
            print(e)

    try:
        print("开始提交")
        db.db_session.commit()
        db.db_session.close()
        print("Succeed!!!")

    except Exception as e:
        print("Failed to commit")
        print(e)