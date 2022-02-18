from tda.auth import easy_clientfrom tda.client import Clientfrom tda.streaming import StreamClientimport asyncioimport jsonimport configfrom datetime import datetimeclient = easy_client(        api_key=config.API_KEY,        redirect_uri=config.REDIRECT_URI,        token_path=config.TOKEN_PATH)stream_client = StreamClient(client, account_id=config.ACCOUNT_ID)def print_message(message):    orderflow_dict = json.loads(json.dumps(message, indent=4))    print(datetime.now())    print(orderflow_dict['content'])    print('\n')async def read_stream():    await stream_client.login()    await stream_client.quality_of_service(StreamClient.QOSLevel.EXPRESS)    # await stream_client.level_one_equity_subs('SPY', fields=[stream_client.LevelOneEquityFields.BID_PRICE])    # Always add handlers before subscribing because many streams start sending    # data immediately after success, and messages with no handlers are dropped.    # stream_client.add_nasdaq_book_handler(print_message)    stream_client.add_level_one_option_handler(print_message)    await stream_client.level_one_option_subs(['SPY_021822P435','AAPL_021822C170'], fields=[stream_client.LevelOneOptionFields.BID_PRICE,                                                                          stream_client.LevelOneOptionFields.ASK_PRICE,                                                                          stream_client.LevelOneOptionFields.LAST_PRICE                                                                          ])    while True:        await stream_client.handle_message()asyncio.run(read_stream())