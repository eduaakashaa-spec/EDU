"""Write app/data/nift/studio.json: NIFT CAT (Creative Ability Test) tasks from the previous papers, restated in short, each with a self-marking rubric.

Run: python tools/nift/make_studio.py
The tasks are practised on paper and marked by the student against the rubric (a computer cannot mark a drawing).
"""
import json
import os

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'app', 'data', 'nift', 'studio.json')

# kind -> rubric of four criteria, 10 marks in all
RUBRICS = {
    'draw': [('Idea', 3, 'The idea is clear and not the first one that comes to mind; it answers the task exactly.'),
             ('Use of the brief', 2, 'Every given condition (theme, shape, number of boxes, words, material) is followed.'),
             ('Drawing and composition', 3, 'Proportion, perspective, line quality and balance of the page.'),
             ('Colour and finish', 2, 'Colour supports the idea, the page is clean, nothing is smudged or half done.')],
    'design': [('Concept', 3, 'A clear user, use and idea; the product solves something.'),
               ('Use of the brief', 2, 'The given shapes, lines or constraints are used as asked (nothing sliced, all used, etc.).'),
               ('Form and proportion', 3, 'The product looks believable: scale, structure, how it is held or used.'),
               ('Colour, render and note', 2, 'Colour and finish suit the user, and the written note is short and clear.')],
    'story': [('Sequence', 3, 'Each step or stage is clearly different from the last and in the right order.'),
              ('Use of the brief', 2, 'The number of boxes, steps or words asked is respected.'),
              ('Drawing clarity', 3, 'Each box can be understood without the caption.'),
              ('Colour and finish', 2, 'Consistent style across boxes; neat.')],
    'write': [('Content', 4, 'Specific, personal and honest; examples from your own life, not general statements.'),
              ('Structure', 3, 'A beginning, a clear order and an end; the main point is easy to find.'),
              ('Language', 2, 'Correct, simple sentences; no repeated words.'),
              ('Length and time', 1, 'Inside the word limit and finished in the time.')],
}

T = [
    ('C01', 'B.Des', 2016, 30, 'draw', 'Colour a transformation', 'Choose two of four themes: a cocoon turning into a butterfly, a leaf from spring to autumn, shiny metal turning to rust, the sky from dawn to night. Colour the boxes to show the change, then justify your choice and process in about 50 words.', 'Colour progression, not drawing, is being tested: plan five or six steps of one colour moving to the next.'),
    ('C02', 'B.Des', 2016, 30, 'draw', 'Feelings in colour only', 'Express any two of astonishment, happiness, rebelliousness and sorrow using colour only, no objects. Justify your choice and process.', 'Use only colour, shape and rhythm of strokes. Decide light or dark, warm or cool, sharp or soft before you start.'),
    ('C03', 'B.Des', 2016, 40, 'design', 'One shape, four products', 'Pick one shape (square, circle, rectangle or triangle) and use it to design four things: a table-top utility product, a textile print, a footwear product and an item of clothing. Draw all four; do not render.', 'Keep the same shape visible in all four. Show the idea in line, with a short label for each.'),
    ('C04', 'B.Des', 2017, 30, 'draw', 'Pairs of opposites', 'Choose one pair of opposites: crispy and soggy, cultured and uncultured, or balanced and unbalanced. Show both sides pictorially in boxes and write a caption under each.', 'Make the two boxes differ in texture, composition and colour so the contrast reads at once.'),
    ('C05', 'B.Des', 2017, 30, 'design', 'T-shirt artwork on a theme', 'Design and colour artwork for a T-shirt on one theme: Music is the Soul of Life, Save the Future of Wildlife, or Dignity for the Aged. Explain the concept in about 50 words.', 'Think about print placement and how few colours it needs; a strong single idea beats a crowded scene.'),
    ('C06', 'B.Des', 2018, 30, 'draw', 'A detailed scene', 'Draw a detailed scene of one: a traffic crossing seen from inside a car, a community festival, or a street play.', 'Show depth (near, middle, far), people with action, and one clear focal point.'),
    ('C07', 'M.Des', 2017, 30, 'write', 'Ten steps of an experience', 'Describe in ten steps your own experience of one of: flying a kite, eating an ice-cream in a cone, bowling.', 'Observation of small details (what the hand, eye and body do) is what is judged; number the steps.'),
    ('C08', 'M.Des', 2017, 40, 'draw', 'Your teacher’s workplace', 'Draw, in detail, the workplace of a teacher you have seen at school or college, with her table and its belongings.', 'Recall is the test: choose a viewpoint, draw the table in perspective, then add objects with their real sizes.'),
    ('C09', 'M.Des', 2017, 30, 'story', 'Six folds of paper', 'Fold a paper six times without tearing it, then draw the unfolding step by step in six boxes.', 'Do it with real paper first; mark the crease lines in each box.'),
    ('C10', 'B.Des', 2019, 30, 'write', 'Pen and paper versus a laptop', 'Write about the difference between writing an essay by hand and typing it directly. Which do you prefer and why? Base it on your own experience. 400 to 500 words.', 'This is a writing task. Give two or three real situations and a clear opinion.'),
    ('C11', 'B.Des', 2019, 30, 'write', 'Blindfolded for a day', 'Imagine you are blindfolded for a day. Discuss five difficult tasks and stress the most difficult one. 400 to 500 words.', 'Use the other senses in your examples, and end with what a designer could change.'),
    ('C12', 'B.Des', 2019, 40, 'design', 'Spectacles for a group', 'Design spectacles for one group: school children, traffic police, sports personalities, or people in public transport. Consider colour, shape, form and proportion.', 'Name the user and the need first (safety, comfort, speed), then let the frame follow.'),
    ('C13', 'B.Des', 2019, 30, 'design', 'An object in 2050', 'Design and colour one object as you imagine it in the year 2050: a door knob, an umbrella or a lunch box. Support it with a tagline.', 'Change something real about how the object works, not only how it looks.'),
    ('C14', 'B.Des', 2019, 30, 'design', 'Design from a given shape', 'Using a shape given in the paper (you may resize and repeat it, but not slice it), design a letter box, a wind chime or a personal computer. Support it with a write-up of about 100 words.', 'Try the shape as a body, a panel and a detail; pick the version that surprises.'),
    ('C15', 'B.Des', 2019, 40, 'story', 'Four stages', 'Draw and colour four stages of one: a bird taking flight from ground to sky, a shirt on a line from wet to dry, or a rose from bud to full bloom.', 'Each stage must show a clear change in shape and colour; keep the same viewpoint.'),
    ('C16', 'B.Des', 2020, 40, 'story', 'A process in four steps', 'Draw the process of one in a four-step sequence in four boxes: folding paper into a boat, or replacing an electric bulb in its holder.', 'Show the hands and the object; choose the four moments that explain the process best.'),
    ('C17', 'B.Des', 2020, 40, 'design', 'A handbag for an occasion', 'Design an interesting handbag for yourself for one occasion: a wedding, a picnic or shopping. Draw and colour a detailed sketch and describe it in four to five sentences.', 'Think about closure, strap, carrying load and material; label two details.'),
    ('C18', 'B.Des', 2023, 40, 'design', 'Design with given lines and shapes', 'Using the lines and shapes given in the paper (which may be repeated, resized or rotated), design one of: an automobile, a piece of utility, or a weighing scale.', 'Use the given pieces as the main structure so the examiner can see them in your design.'),
    ('C19', 'M.Des', 2023, 30, 'design', 'Multi-function product or pandemic tagline', 'Either design a multi-task product (a workout bench or a boat) for small homes, or use two words from a given pandemic word list to write a tagline for an airline or a brand and make a one-page advertisement.', 'Pick the option you can finish well in the time. Show how the product folds, stacks or changes use.'),
    ('C20', 'B.Des', 2026, 40, 'design', 'A birdfeeder from shapes', 'Design a birdfeeder for outside a window using all the given shapes at least once (size may change, no cutting the shapes), for one setting: a rooftop restaurant, a meditation centre, an author’s office or an old age home.', 'Make the setting visible in the mood, colour and scale of the feeder.'),
    ('C21', 'B.Des', 2026, 30, 'draw', 'A festive season, pencil colour only', 'Draw and render a festive season in a village marketplace, a forest nature retreat or a riverside celebration, using pencil colours only.', 'Pencil colour rewards layering: light first, then build depth.'),
    ('C22', 'B.Des', 2026, 30, 'design', 'Transform an everyday object', 'Take inspiration from a water tap, a stool or a bicycle and design a product for a street vendor, an elderly person or an office worker, showing a proper transformation of the chosen object and the product in use with the user.', 'Show the original object, the changed product and the user on one page.'),
]


def main():
    tasks = []
    for tid, prog, year, marks, kind, title, prompt, tip in T:
        tasks.append({'id': tid, 'prog': prog, 'year': year, 'marks': marks, 'kind': kind, 'title': title, 'prompt': prompt, 'tip': tip,
                      'rubric': [{'k': k, 'max': m, 'd': d} for k, m, d in RUBRICS[kind]]})
    for t in tasks:
        assert sum(r['max'] for r in t['rubric']) == 10, t['id']
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, 'w', encoding='utf-8') as f:
        json.dump(tasks, f, indent=1, ensure_ascii=False)
    print(len(tasks), 'tasks ->', OUT)


if __name__ == '__main__':
    main()
