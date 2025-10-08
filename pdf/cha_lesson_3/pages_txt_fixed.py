from pathlib import Path
from typing import List

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas

# Исправленные тексты (сопоставлены с изображениями pdf/1.jpg ... 6.jpg)
# Форматирование простое: сохраняем строки и пустые строки, используем моноширинный шрифт.

part_1 = '''
Part One: Expressions (Items 1-15)
Choose the best answer.

1. A: Could I use your phone for a moment?
   B: ____. Help yourself.

   1. By all means
   2. Not at all
   3. I'm afraid not
   4. That's alright
   5. Never mind it

2. A: I think I have an appointment with Mr. Johnson at 3 p.m. today. Is that right?
   B: ____, please. Let me check the timetable first. Yes, that's right.

   1. Hold up
   2. Hang up
   3. Hold on
   4. Hang out
   5. Hold back

3. A: That salad was delicious. ____?
   B: Oh, it's very easy. Do you want to write it down?
   A: Yes, I will.

   1. How is it
   2. How do you make it
   3. How do you do it
   4. How long does it take
   5. How does it taste

4. A: I heard that there's a big sale this weekend. Do you want to go shopping?
   B: ____. I'm broke.
   A: Well, we can still do some window shopping, can't we?

   1. I feel bad
   2. I don't care
   3. I'd love to
   4. I don't like it
   5. I don't feel like it
'''

part_2 = '''
5-8:

Lucy: You look tired. ____5____ last night?
Paul: No. I had a bunch of my friends over and we partied until the wee hours.
Lucy: ____6____ you look so bad!
Paul: I guess I just can't take late nights like I used to. My head is spinning and I have a migraine.
Lucy: I think you need to go home and take a rest.
Paul: ____7____. But I don't think I can keep my eyes open long enough to drive home.
Lucy: Don't worry. I'll ____8____. But next time, watch the partying, OK?

5. 1. What did you do
   2. Did you stay here
   3. Who did you meet
   4. Didn't you get enough sleep
   5. When did you sleep

6. 1. No way
   2. No need
   3. No chance
   4. No reason
   5. No wonder

7. 1. I'll do that
   2. Yes, I do
   3. I wish I could
   4. No, I don't
   5. I'm not in the mood

8. 1. wake you up
   2. keep my eyes open
   3. stay with you
   4. keep an eye on you
   5. give you a ride home
'''

part_3 = '''
9-12:

Amy: ____9____ between you and Brian? Did you guys have a fight or something?
John: I can't ____10____. He has such a short fuse that even a little piece of friendly advice sets him off.
Amy: So what did you tell him?
John: I told him that if he could ____11____ and try not to lose his temper so easily,
he would be more popular.
Amy: No wonder he threw a fit. His popularity is really a sore spot.
John: Well, I guess I'll just ____12____. That'll teach me to give advice!
Amy: Not unless you want to die!
'''

part_4 = '''
9.

1. What's the story
2. What's missing
3. What's the point
4. What's going on
5. What's the relationship

10.

1. let him down
2. stand him anymore
3. figure him out
4. wait for him anymore
5. apologize to him

11.

1. show up
2. step in
3. hang in there
4. stay still
5. be more patient

12.

1. keep my head cool
2. keep pushing it
3. keep my mouth shut
4. keep pressuring it
5. keep my fingers crossed

13-15:

Jan: Gary, you look so worried. What happened?
Gary: Well, I want to get into that class, but I just found out that there are so many people on the waiting list. I guess ____13____.
Jan: ____14____! Many people might drop the class and then there will be some openings. You never know.
Gary: I hope so.
Jan: Come on, cheer up. Don't worry so much. ____15____.

13.

1. I might drop out
2. chances are probably slim
3. I should forget about it
4. it's time to consider another class
5. I have no opportunities

14.

1. I wouldn't care
2. I wouldn't try
3. I wouldn't bother
4. I wouldn't dare
5. I wouldn't say that

15.

1. I believe in it
2. Everything will change
3. You're hopeless
4. Everything will work out just fine
5. Just leave it to chance
'''

part_5 = '''
Part Two: Vocabulary (Items 16-30)
Items 16-25: Meaning in Context
Choose the best alternative to make the sentence(s) meaningful.

16. Experiments are often ____ in a laboratory under controlled conditions.

1. discussed
2. debated
3. conducted
4. criticized
5. mentioned

17. The greatest physical ____ between humans and apes is the hollow space humans have under their chins.

1. danger
2. comfort
3. therapy
4. distinction
5. attraction

18. ____, only two students signed up to help the children at the orphanage. However, more students signed up later on.

1. Initially
2. Certainly
3. Basically
4. Primarily
5. Eventually

19. To ____ discipline, the principal punishes students who are late for school by making them clean the canteen on Saturday.

1. enforce
2. accept
3. monitor
4. estimate
5. implement

20. The football match was ____ as most of the players had fallen ill.

1. called away
2. called in
3. called on
4. called up
5. called off

21. Explanations given to the patient by the anesthetist prior to surgery often ____ anxiety and ____ the need for analgesics or painkillers.

1. ignore - prevent
2. relieve - reduce
3. explore - prepare
4. parallel - assume
5. intensify - counteract
'''

part_6 = '''
22. According to Hume, it is not logic that determines what we say and do; if we decide to help a person in need, we do so because of our ____, not our ____.

1. concern - kindness
2. duty - rights
3. beliefs - convictions
4. feelings - reason
5. consciousness - emotions

23. Although they are ____ by traps, poison, and shotguns, predators ____ to feast on flocks of sheep.

1. lured - refuse
2. harmed - hesitate
3. destroyed - cease
4. impeded - continue
5. encouraged - attempt

24. Employers who retire people who are willing and able to continue working should realize that ____ age is not an effective ____ in determining whether an individual is capable of working.

1. physical - barrier
2. advanced - method
3. intellectual - factor
4. deteriorating - value
5. chronological - criterion

25. Using computer labs to ____ classroom instruction is most effective when the curriculum ____ lab exercises and classroom teaching in a coordinated manner.

1. foster - curtails
2. supplement - integrates
3. minimize - reinforces
4. substantiate - undermines
5. remedy - compromises
'''

part_7 = '''
Items 26-30: Meaning Recognition
Choose the alternative which has the same meaning as the underlined word in the given sentence.

26. Most customers were satisfied with the way their complaints were handled.

1. Computers can handle huge amounts of data.
2. She cannot handle it when people criticize her.
3. Please handle the fruit carefully or it will bruise.
4. The headmaster handled the situation very well.
5. We teach the children to handle the animals gently.

27. The principal took the position that the students did not need music classes.

1. All parking signs have now been placed in position.
2. My elder brother is thinking of applying for that position.
3. No one was sure of the chairperson's position on any issue.
4. Our hotel was in a superb central position near Siam Square.
5. John took up his new position as sales manager in September.

28. The Bureau is active in promoting overseas investment.

1. The virus is active even at low temperatures.
2. This lady took an active interest in local charities.
3. The disease remains active throughout the patient's life.
4. Meditation techniques help keep the mind active and alert.
5. The volcano became active last year with a series of eruptions.

29. He was surprised to learn that she was a lot older than he had thought.

1. Your homework for today is to learn the periodic table.
2. We learned about our appointment by telephone yesterday.
3. They have to learn that they cannot just do whatever they like.
4. The actors hardly had time to learn their lines before filming started.
5. Youngsters must learn what is dangerous and what is not to be feared.

30. The data will cover things such as water currents and wind direction.

1. Strong currents can be very dangerous for swimmers.
2. There was a strong current of opinion in favor of war.
3. The student movement formed a distinct current of protest.
4. Magnetic fields are produced by currents flowing in the cables.
5. The battery supplies current for the operation of the starting motor.
'''


def make_text_pdf(text_blocks: List[str], out_path: Path) -> Path:
    c = canvas.Canvas(str(out_path), pagesize=A4)
    w, h = A4
    margin_x, margin_y = 20 * mm, 20 * mm
    line_height = 14
    c.setFont("Courier", 11)

    for block_idx, block in enumerate(text_blocks, start=1):
        y = h - margin_y
        for line in block.splitlines():
            if line.strip() == "":
                y -= line_height
                if y < margin_y:
                    c.showPage();
                    c.setFont("Courier", 11);
                    y = h - margin_y
                continue
            if y < margin_y:
                c.showPage();
                c.setFont("Courier", 11);
                y = h - margin_y
            c.drawString(margin_x, y, line)
            y -= line_height
        if block_idx < len(text_blocks):
            c.showPage();
            c.setFont("Courier", 11)
    c.save()
    return out_path


if __name__ == "__main__":
    base = Path(__file__).parent
    out_pdf = base / "CHA_Lesson_3_Text_punct_v2.pdf"
    parts = [part_1, part_2, part_3, part_4, part_5, part_6, part_7]
    make_text_pdf(parts, out_pdf)
    print(f"✅ Готово: {out_pdf.resolve()}")
