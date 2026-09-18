#!/usr/bin/python3

from renderlib import *
from easing import *

# code and artwork by mole

# URL to Schedule-XML
scheduleUrl = 'https://datenspuren.de/2018/fahrplan/schedule.xml'

def introFrames(args):
# (0.5 sec) show loading text
  frames = int(fps/2)
  loading=6+1  
  r = range(0, frames)
  for i in r:
    n = int(((loading/frames)*i)) if (i < r[-1]) else loading;
    yield (
      ('t-loading-'+str(n), 'style', 'display',  'inline'),
    )

# (3 sec) loading progress bar
  frames = 3*fps
  overlaysize = 1280
  display = 'inline';
  r = range(0, frames)
  for i in r:
    overlaypos = easeInCubic(i, 0, overlaysize, frames) if (i < r[-1]) else overlaysize
    if (i % 4 == 0):
      display =  'inline' if (display == 'none') else 'none';
    else:
      display = 'inline' if (i == r[-1]) else display

    yield (
      ('g-t-loading', 'style', 'display', display),
      ('overlay', 'attr', 'transform', 'translate(%.4f, 0)' % (overlaypos)),
    )

# (1 sec) move loading text to ds text coords
  frames = int(1*fps)
  loadingXdelta = 265.331+50
  loading -= 1
  r = range(0, frames)
  for i in r:
    loadingpos = easeInQuad(i, 0, loadingXdelta, frames) if (i < r[-1]) else loadingXdelta  
    n = abs(int((loading/frames*i)-loading))+1
    loadingdisplay = 'none' if (n != abs(int((loading/frames*(i+1))-loading))+1) or (i == r[-1]) else 'inline'
    yield (
      ('g-t-loading', 'attr', 'transform', 'translate(-%.4f, 0)' % (loadingpos)),
      ('t-loading-'+str(n), 'style', 'display',  loadingdisplay),
    )

# (1 sec) show ds2018 text
  frames = int(1*fps)
  datenspuren = 10+1
  t2018Xdelta = 462.583
  r = range(0, frames)
  for i in r:
    n = int((datenspuren/frames)*i) if (i < r[-1]) else datenspuren
    t2018pos = easeInCubic(i, 0, t2018Xdelta, frames) if (i < r[-1]) else t2018Xdelta
    t2018opacity = easeInQuad(i, 0, 1, frames) if (i < r[-1]) else 1
    inlayopacity = easeInQuad(i, 1, -1, frames) if (i < r[-1]) else 0
    yield (
      ('t-datenspuren-'+str(n), 'style', 'display',  'inline'),
      ('t-2018', 'attr', 'transform', 'translate(%.4f, 0)' % (t2018pos)),
      ('t-2018', 'style',  'opacity',  '%.4f' % (t2018opacity)),
      ('inlay-19', 'style',  'opacity', '%.4f' % (inlayopacity)),      
    )

# (1 sec) move logo up
  frames = 1*fps
  logoYdelta = 260
  r = range(0, frames)
  for i in r:
    logopos = easeInQuad(i, 0, logoYdelta, frames) if (i < r[-1]) else logoYdelta
    yield (
      ('g-logo', 'attr', 'transform', 'translate(0, -%.4f)' % (logopos)),
    )

# (1 sec) swipe info background
  infosize = 1280
  frames = 1*fps
  r = range(0, frames)
  for i in r:
    infopos = i * (infosize / frames) if (i < r[-1]) else infosize;
    yield (
      ('bginfo', 'attr', 'transform', 'translate(%.4f, 0)' % (infopos)),
    )
        
# (1 sec) show data about talk
  frames = 1*fps
  r = range(0, frames)
  for i in r:
    opacity = easeInQuad(i, 0, 1, frames) if (i < r[-1]) else 1
    yield (
      ('t-id', 'style', 'opacity', '%.4f' % (opacity)),
      ('t-title', 'style', 'opacity', '%.4f' % (opacity)),
      ('t-subtitle', 'style', 'opacity', '%.4f' % (opacity)),  
    )
    
# (1 sec) animate spacer and bounce names in
  frames = 1*fps
  spsize = 360
  speakerXdelta = 1920-50
  r = range(0, frames)
  for i in range(0, frames):
    sppos = i * (spsize / frames) if (i < r[-1]) else spsize
    speakerpos =  i * ( speakerXdelta/ frames) if (i < r[-1]) else speakerXdelta
    yield (
      ('spacer', 'attr', 'transform', 'translate(%.4f, 0)' % (sppos)),
      ('g-t-speaker', 'attr', 'transform', 'translate(-%.4f, 0)' % (speakerpos)),
    )
    
# (2 sec) show hackspace logos
  frames = 2*fps
  r = range(0, frames)
  for i in r:
    opacity = easeInCubic(i, 0, 1, frames) if (i == r[-1]) else 1
    yield (
      ('c3d2', 'style', 'opacity', '%.4f' % (opacity)),
      ('t-zentralwerk', 'style', 'opacity', '%.4f' % (opacity)),
    )
    
# (3 sec) wait some frames for reading the info texts
  frames = 3*fps
  beep = 0
  dir = 1
  r = range(0, frames)
  for i in r:
    yield(
      ('hb-'+str(beep+1),'style', 'display',  'none'),
      ('hb-'+str(beep), 'style', 'display',  'inline'),
      ('hb-'+str(beep-1),'style', 'display',  'none'),
    )
    if (i % 3 == 0):
      # direction
      if (beep == 24):
        dir = 0
      elif (beep == 0) and (i != 3):
        dir = 1
        
      # heartbeep
      if (dir == 1):
        beep += 1
      else:
        beep -= 1
    # last frame
    if (i == r[-int(frames/fps)-1]):
      beep == 0;
    # cut turn around frames
    if (i == r[-int(frames/fps)]):
      break    

def backgroundFrames(parameters):
# (24 sec + 1frame) heartbeat
  frames = 24*fps
  beep = 0
  dir = 1
  r = range(0, frames)
  for i in r:
    yield(
      ('hb-'+str(beep+1),'style', 'display',  'none'),
      ('hb-'+str(beep), 'style', 'display',  'inline'),
      ('hb-'+str(beep-1),'style', 'display',  'none'),
    )
    if (i % 3 == 0):
      # direction
      if (beep == 24):
        dir = 0
      elif (beep == 0) and (i != 3):
        dir = 1
        
      # heartbeep
      if (dir == 1):
        beep += 1
      else:
        beep -= 1
    # cut over lapping frames coz of turnaround 
    if (i == r[-24]):
      break
              
       
def outroFrames(args):
# (2 sec) hide 2018 text
  frames = int(2*fps)
  datenspuren = 10+1
  r = range(0, frames)
  for i in range(0, frames):
    n = abs(int((datenspuren/frames)*i)-datenspuren) if (i < r[-1]) else 1
    t2018opacity = easeInQuad(i, 1, -1, frames) if (i < r[-1]) else 0
    inlayopacity = easeInCubic(i, 0, 1, frames) if (i < r[-1]) else 1
    yield(
      ('t-2018', 'style', 'opacity', '%.4f' % (t2018opacity)),
      ('inlay-19', 'style', 'opacity', '%.4f' % (inlayopacity)),
      ('t-datenspuren-'+ str(n), 'style', 'display',  'none'),
    )
    
# (1 sec) fade unloading text
  frames = int(1*fps)
  loading = 9
  r = range(0, frames)
  for i in r:
    n = int((loading/frames)*i) if (i < r[-1]) else loading
    yield (
      ('t-loading-'+str(n), 'style', 'display',  'inline'),
    )
    
# (2 sec) unloading progress bar
  frames = 2*fps
  overlaysize = 1280
  display = 'inline';
  n = 0
  r = range(0, frames)
  for i in r:
    overlaypos = easeInQuad(i, 0, overlaysize, frames) if (i < r[-1]) else overlaysize
    logoopacity = easeInCubic(i, 1, -1, frames) if (i < r[-1]) else 0
    if (i < r[-int(frames/6)]):
      c3d2opacity = 0
    else:
      c3d2opacity = easeInQuad(n, 0, 1, int(frames/6))  if (i < r[-1]) else 1
      n += 1    

    if (i % 4 == 0):
      display =  'inline' if (display == 'none') else 'none'
    
    yield (
      ('g-t-loading', 'style', 'display', display),
      ('overlay', 'attr', 'transform', 'translate(-%.4f, 0)' % (overlaypos)),
      ('g-logo', 'style', 'opacity', '%.4f' % (logoopacity)),
      ('c3d2', 'style', 'opacity',  '%.4f' % (c3d2opacity)),
    )
    
# (1 sec) c3d2 logo        
  frames = 2*fps
  n = 0
  r = range(0, frames)
  for i in range(0, frames):
    c3d2opacity = easeInQuad(i, 1, -1, frames) if (i < r[-1]) else 0
    if (i < r[-int(frames/2)]):
      datenknotenopacity = 0
    else:
      datenknotenopacity = easeInQuad(n, 0, 1, int(frames/2))  if (i < r[-1]) else 1
      n += 1      

    yield(
      ('c3d2', 'style', 'opacity', '%.4f' % (c3d2opacity)),
      ('g-datenknoten', 'style', 'opacity', '%.4f' % (datenknotenopacity)),
    )

# (1 sec) datenknoten
  frames = 1*fps
  n = 0
  r = range(0, frames)
  for i in range(0, frames):
    datenknotenopacity = easeInQuad(i, 1, -1, frames) if (i < r[-1]) else 0
    if (i < r[-int(frames/2)]):
      bysaopacity = 0    
    else:
      bysaopacity = easeInQuad(n, 0, 1, int(frames/2)) if (i < r[-1]) else 1
      n += 1

    yield(
      ('g-datenknoten', 'style', 'opacity', '%.4f' % (datenknotenopacity)),
      ('g-bysa', 'style', 'opacity',  '%.4f' % (bysaopacity)),
    )

# (2 sec) by sa
  frames = 2*fps
  n = 0
  r = range(0, frames)
  for i in range(0, frames):
    if (i < r[-int(frames/4)]):
      bysaopacity = 1    
    else:
      bysaopacity = easeInQuad(n, 1, -1, int(frames/4)) if (i < r[-1]) else 0
      n += 1  

    yield(
      ('g-bysa', 'style', 'opacity', '%.4f' % (bysaopacity)),
    )
  
      
def pauseFrames(args):
# same as background
  frames = 24*fps
  beep = 0
  dir = 1
  r = range(0, frames)
  for i in r:
    yield(
      ('hb-'+str(beep+1),'style', 'display',  'none'),
      ('hb-'+str(beep), 'style', 'display',  'inline'),
      ('hb-'+str(beep-1),'style', 'display',  'none'),
    )
    if (i % 3 == 0):
      # direction
      if (beep == 24):
        dir = 0
      elif (beep == 0) and (i != 3):
        dir = 1
        
      # heartbeep
      if (dir == 1):
        beep += 1
      else:
        beep -= 1
    # cut over lapping frames coz of turnaround 
    if (i == r[-24]):
      break


def debug():
    render('intro.svg',
        '../intro.ts',
        introFrames,
        {
            '$id': 7776,
            '$title': 'StageWar live on stage!',
            '$subtitle': 'Metal Konzert - with a long subtitle title that has a tittle which has a long title that is titled until the title breaks the line',
            '$persons':  'one girl, another guy and a crowd'
        }
    )

    # render('outro.svg',
        # '../outro.ts',
        # outroFrames
    # )

    # render(
        # 'background.svg',
        # '../background.ts',
        # backgroundFrames
    # )

    # render('pause.svg',
        # '../pause.ts',
        # pauseFrames
    # )

def tasks(queue, args, idlist, skiplist):
    # iterate over all events extracted from the schedule xml-export
    for event in events(scheduleUrl):
        # if event['room'] not in ('Chirurgie (Saal 1.04)', 'Kreißsaal (Saal 1.11)'):
            # print("skipping room %s (%s [%s])" % (event['room'], event['title'], event['id']))
            # continue
        # if not (idlist==[]):
                # if 000000 in idlist:
                        # print("skipping id (%s [%s])" % (event['title'], event['id']))
                        # continue
                # if int(event['id']) not in idlist:
                        # print("skipping id (%s [%s])" % (event['title'], event['id']))
                        # continue

        # generate a task description and put them into the queue
        queue.put(Rendertask(
            infile = 'intro.svg',
            outfile = str(event['id'])+".ts",
            sequence = introFrames,
            parameters = {
                '$id': event['id'],
                '$title': event['title'],
                '$subtitle': event['subtitle'],
                '$persons': event['personnames']
            }
        ))

    # place a task for the outro into the queue
    if not "out" in skiplist:
        queue.put(Rendertask(
            infile = 'outro.svg',
            outfile = 'outro.ts',
            sequence = outroFrames
         ))

    # place the pause-sequence into the queue
    if not "pause" in skiplist:
        queue.put(Rendertask(
            infile = 'pause.svg',
            outfile = 'pause.ts',
            sequence = pauseFrames
        ))

    # place the background-sequence into the queue
    if not "bg" in skiplist:
        queue.put(Rendertask(
            infile = 'background.svg',
            outfile = 'background.ts',
            sequence = backgroundFrames
        ))
