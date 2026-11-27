# manual labels from montages (order = montage_sel.json order). (type, dof 0/1/2 or None, cam, horizon_y or None)
# type C close-up, M medium, W wide, X macro/object; cam L low, E eye, H high; None dof = crossfade/skip
M1=[('M',0,'E',None),('C',1,'E',None),('W',0,'E',None),('M',1,'E',None),('M',0,'E',None),('W',0,'L',.40),('M',0,'L',.42),('C',0,'E',None),
('W',0,'E',None),('W',0,'H',None),('M',0,'H',None),('C',2,'E',None),('M',0,'H',None),('M',0,'E',None),('X',0,'H',None),('M',0,'L',None),
('W',0,'E',None),('X',1,'E',None),('M',0,'E',None),('W',0,'L',.65),('M',0,'L',None),('W',1,'L',.55),('W',0,'E',None),('M',1,'E',None),
('W',0,'E',None),('W',0,'E',None),('M',2,'E',None),('M',1,'E',.33),('M',0,'E',None),('M',0,'E',None),('C',1,'E',None),('M',0,'E',None),
('W',0,'H',None),('W',0,'H',None),('M',0,'E',None),('W',0,'L',None),('X',2,'E',None),(None,None,None,None),('M',0,'E',None),('M',0,'E',None)]
M2=[('C',1,'E',None),('X',0,'E',None),('X',0,'E',None),(None,None,None,None),('W',0,'L',None),('M',0,'E',None),('M',1,'H',None),('W',0,'E',None),
('W',1,'H',None),('C',1,'E',None),('C',1,'E',None),(None,None,None,None),('C',1,'E',None),('M',0,'L',None),('W',0,'E',None),('M',0,'E',None),
('M',1,'E',None),('M',0,'H',None),('C',2,'E',None),('C',1,'E',None),('X',0,'E',None),('X',0,'E',None),('M',0,'H',None),('M',0,'L',None),
('M',0,'L',.25),('W',0,'E',.50),('W',0,'H',None),('M',0,'E',None),('M',0,'E',None),('X',0,'E',None),('M',0,'L',.25),('M',0,'E',None),
('W',0,'E',None),('W',0,'H',None),('W',1,'E',.30),('W',0,'H',None),('M',0,'E',None),('W',0,'E',None),('W',0,'E',None),('C',1,'E',None)]
M3=[('M',0,'L',None),('W',0,'H',.20),('M',0,'E',.25),('W',0,'L',.43),('C',0,'E',None),('C',0,'E',None),('W',0,'E',None),('M',0,'E',None),
('X',1,'E',None),('X',1,'E',None),('M',0,'H',None),('W',0,'L',.25),('W',0,'H',None),('C',1,'E',None),('W',0,'H',None),('M',0,'E',None),
('W',0,'L',.40),('W',0,'H',None),('W',0,'L',.35),('W',0,'L',.45),('C',0,'E',None),('X',0,'E',None),('M',0,'E',None),('M',0,'E',None),
('M',0,'E',None),('X',0,'E',None),('C',0,'E',None),(None,None,None,None),('X',0,'E',None),('X',0,'E',None),('M',0,'E',None),('M',0,'L',None),
('M',0,'H',None),('W',0,'H',None),('W',0,'H',None),('C',1,'E',None),('W',0,'H',None),('W',0,'H',None),('M',1,'E',None),('M',0,'E',.38)]
LAB=M1+M2+M3
