## WE LOVE GAMBLING
Suht lihtne ja labane lahendus dobotile blackjacki mängimiseks. Video (hasartmängule kaasa elamiseks): https://youtu.be/V2wHL51SkAk
# -setup-
1) Model visualisation kasutab [Teodor Kostadinovi kaardituvastuslahendust](https://github.com/TeogopK/Playing-Cards-Object-Detection), sealt on vaja hankida [sünteetiline dataset](https://github.com/TeogopK/Playing-Cards-Object-Detection/blob/main/final_models/yolov8m_synthetic.pt) ning model_visualisation2.py  "model_path": muutuja suunata selleni
2) Dobot studios on vaja avada fail dobotbj.py ning ühendada programm dobotiga
3) Peale doboti ühendamist on vaja ühendada arvutiga 2 kaamerat, cam1 on dobot, cam0 on dealer
4) Mõlemad failid on vaja suunata sama tekstifaili poole, kus dobot saab kaardid kätte. meie näites muutuja fail ("detected_cards.txt")
5) Esmalt käivitada model_visualisation2.py ning oodata kuni 2 kaamerapilti ilmuvad
6) Seejärel võib käivitada doboti programmi ning mängima asuda (inimene käitub kui diiler... duh)
