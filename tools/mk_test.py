import unittest
from mk import html_2_markdown

class MyTestCase(unittest.TestCase):
    # 该方法会首先执行，方法名固定
    def setUp(self):
        pass

    # 该方法会在测试代码执行完后执行，方法名固定
    def tearDown(self):
        pass

    def test_html_2_markdown(self):
        _html = """
 <link rel="stylesheet" href="p.css"/><div class="hwrap"><h2>can</h2><div class="git"><span class="ipa">[kæn]</span></div><hr/></div><link rel="stylesheet" href="c.css"/><link rel="stylesheet" href="v.css"/><link rel="stylesheet
" href="cls.css"/><link rel="stylesheet" href="mw.css"/><link rel="stylesheet" href="o.css"/><link rel="stylesheet" href="l.css"/><link rel="stylesheet" href="d.css"/><div class="pf"><a class="Sizev" href="sound://sndccacan.spx"><im
g src="v.png"></a><a class="amefile" href="sound://ameProns/l3can.mp3"><img src="lus.png"></a><a class="amefile" href="sound://ameProns/l3can2.mp3"><img src="lus.png"></a><a class="amefile" href="sound://ameProns/l3can3.mp3"><img sr
c="lus.png"></a><a class="Sizecus" href="sound://us_pron/can.mp3"><img src="cus.png"></a><a class="Sizeous" href="sound://mediaenglishus_pronccancan__can__us_1.spx"><img src="ous.png"></a><a class="Sizeous" href="sound://mediaenglis
hus_pronccancan__can__us_2.spx"><img src="ous.png"></a><a class="Sizeclus" href="sound://COLmp3en_us_can.spx"><img src="clus.png"></a><a class="Sizeclus" href="sound://COLmp3en_us_can_1.spx"><img src="clus.png"></a><a class="mw" hre
f="sound://mw_can.spx"><img src="mw.png"></a><a class="Sized" href="sound://C0078900.spx"><img src="d.png"></a><a class="Sized" href="sound://C0079000.spx"><img src="d.png"></a><a class="brefile" href="sound://breProns/ld44can.mp3">
<img src="luk.png"></a><a class="brefile" href="sound://breProns/brelasdecan1.mp3"><img src="luk.png"></a><a class="Sizeouk" href="sound://mediaenglishuk_pronccancan__can__gb_1.spx"><img src="ouk.png"></a><a class="Sizeouk" href="so
und://mediaenglishuk_pronccancan__can__gb_2.spx"><img src="ouk.png"></a><a class="Sizecuk" href="sound://uk_pron/ukcamsh002.mp3"><img src="cuk.png"></a><a class="Sizecluk" href="sound://COLmp307712.spx"><img src="cluk.png"></a><a class="Sizecluk" href="sound://COLmp3en_gb_w0012950.spx"><img src="cluk.png"></a><a class="Sizecluk" href="sound://COLmp307597.spx"><img src="cluk.png"></a><a class="Sizeclunkn" href="sound://COLmp364374.spx"><img src="clunkn.png"></a/span><span class="label label-success">CET6</span><span class="label label-info">TEM4</span><span class="label label-warning">考研</span><div class="level level1"><div class="round roundRed"></div></div><div class="level level2"><d class="round roundRed"></div></div><div class="level level3"><div class="round roundRed"></div></div><div class="level level4"><div class="round roundRed"></div></div><div class="level level5"><div class="round roundRed"></div></div></div><div class="coca"><span class="pos">n</span><span class="rank">2967</span><div class="total">11458</div><div class="table"><div class="spoken"><div class="freq">1325</div></div><div class="fiction"><div class="freq">4133</div></div><div class="magazine"><div class="freq">3200</div></div><div class="newspaper"><div class="freq">1898</div></div><div class="academic"><div class="freq">902</div></div></div><span class="pos">v</span><span class="rank">37</span><div class="total">1106769</div><div class="table"><div class="spoken"><div class="freq">278415</div></div><div class="fiction"><div class="freq">177558</div></div><div class="magazine"><div class="freq">268509</div></div><div class="newspaper"><div class="freq">183652</div></div><div class="academic"><div class="freq">198635</div></div></div></div><div class="coca iweb"><span class="pos">VERB</span><span class="rank">25</span><div class="total">55412781</div><span class="pos">NOUN</span><span class="rank">3183</span><div class="total">365955</div></div><div class="coca2">能(<font color=orangered>50%</font>)，可以(<font color=orangered>44%</font>)，罐头(<font color=orangered>5%</font罐装(<font color=orangered>1%</font>)</div><div class="gdc"><div class="dcb"><span class="pos">aux.</span><span class="dcn">能； 能够； 可以； 可能</span></div><div class="dcb"><span class="pos">n.</span><span class="dcn">罐头； （用铁或其他金属制作的）食品罐头</span></div><div class="dcb"><span class="pos">vt.</span><span class="dcn">将…装入密封罐中保存</span></div></div><script src="config.ini"></script><script src="fy.js"></script>
        """
        _result = html_2_markdown(_html)
        # todo 使用class选择器 选择class="coca iweb" class="coca2" class="gdc"
        # 只选出上述3个进行html转markdown操作
        print(_result)



if __name__ == '__main__':
    unittest.main()
