from src.ai_inference.utils.tools import dotdict


def get_lstm_default() -> dotdict:
    args = dotdict()

    args.model = 'informer'  # model of experiment, options: [informer, informerstack, informerlight(TBD)]

    args.data = 'custom'  # data
    args.root_path = 'D:/pythonProject/Informer2020/output/crypto_eth_kline_minutes_24m_1698767999000end'  # root path of data file
    args.data_path = '0.csv'  # data file
    args.features = 'M'  # forecasting task, options:[M, S, MS]; M:multivariate predict multivariate, S:univariate predict univariate, MS:multivariate predict univariate
    args.target = 'close_price'  # target feature in S or MS task
    args.freq = 's'  # freq for time features encoding, options:[s:secondly, t:minutely, h:hourly, d:daily, b:business days, w:weekly, m:monthly], you can also use more detailed freq like 15min or 3h
    args.checkpoints = 'D:/pythonProject/Informer2020/informer_checkpoints'  # location of model checkpoints

    args.seq_len = 96  # 336  # input sequence length of Informer encoder
    args.label_len = 48  # 48 #336  # start token length of Informer decoder
    args.pred_len = 10  # 720  # prediction sequence length 预测的时刻数，如果freq=h，设置24，表示预测24小时
    # Informer decoder input: concat[start token series(label_len), zero padding series(pred_len)]

    args.enc_in = 4  # encoder input size
    args.dec_in = 4  # decoder input size
    args.c_out = 4  # output size #输出也是7个维度
    args.factor = 5  # probsparse attn factor
    args.d_model = 512  # dimension of model
    args.n_heads = 8  # num of heads
    args.e_layers = 2  # num of encoder layers
    args.d_layers = 1  # num of decoder layers
    args.d_ff = 2048  # dimension of fcn in model
    args.dropout = 0.05  # dropout
    args.attn = 'prob'  # attention used in encoder, options:[prob, full]
    args.embed = 'timeF'  # time features encoding, options:[timeF, fixed, learned]
    args.activation = 'gelu'  # activation
    args.distil = True  # whether to use distilling in encoder
    args.output_attention = False  # whether to output attention in ecoder

    args.batch_size = 32
    args.learning_rate = 0.0001
    args.loss = 'mse'
    args.lradj = 'type1'
    args.use_amp = False  # whether to use automatic mixed precision training
    args.s_layers = '3,2,1'

    args.num_workers = 0
    args.itr = 1
    args.train_epochs = 2
    args.patience = 3
    args.des = 'exp'

    args.use_gpu = True if torch.cuda.is_available() else False
    args.gpu = 0

    args.use_multi_gpu = False
    args.devices = '0,1,2,3'

    args.use_gpu = True if torch.cuda.is_available() and args.use_gpu else False

    args.padding = 0

    args.save_interval = 180  # 保存周期秒数
    args.scale = True  # 数据是否归一化处理

    args.resume = True  # 续训模式
    args.task_name = args.model
    args.use_wandb = False  # 是否使用wandb
    # 多gpu的适配
    # if args.use_gpu and args.use_multi_gpu:
    #     args.devices = args.devices.replace(' ', '')
    #     device_ids = args.devices.split(',')
    #     args.device_ids = [int(id_) for id_ in device_ids]
    #     args.gpu = args.device_ids[0]
    #
    # args.detail_freq = args.freq  # 带数量的时间频率
    # args.freq = args.freq[-1:]  # 纯单位的时间频率

    return args