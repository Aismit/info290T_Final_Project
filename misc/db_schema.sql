CREATE TABLE players (
  Id INT, Id2 INT, Player VARCHAR(250), Pos VARCHAR(10), Age FLOAT, Tm VARCHAR(10),
  G FLOAT, GS FLOAT, MP FLOAT, FG FLOAT, FGA FLOAT, FGPCT FLOAT, 3P FLOAT, 3PA FLOAT,
  3PPCT FLOAT, 2P FLOAT, 2PA FLOAT, 2PPCT FLOAT, eFGPCT FLOAT, FT FLOAT, FTA FLOAT,
  FTPCT FLOAT, ORB FLOAT, DRB FLOAT, TRB FLOAT, AST FLOAT, STL FLOAT, BLK FLOAT,
  TOV FLOAT, PF FLOAT, PTS FLOAT, first VARCHAR(125), last VARCHAR(125)
);

CREATE TABLE games (
  Id INT, Date VARCHAR(20), Start_ET VARCHAR(10), Visitor VARCHAR(10), VisitorPTS INT,
  Home VARCHAR(10), HomePTS INT, OT INT, Attendance INT
);
