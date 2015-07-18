Title: Java Rx with live financial market data from IB 
Date: 2015-07-17 16:20
Category: Java 


In one of my recent projects I automated a trading strategy using [Iteractive Brokers](https://www.interactivebrokers.com/en/?f=%2Fen%2Fsoftware%2Fibapi.php&ns=T) Java API,
 the perfect companion framework  to handle large amount if  live and historical data  is
[RxJava](https://github.com/ReactiveX/RxJava). 
Reading the doc and examples of RXJava can be intimidating and quite abstract, here is a hands on example of how to use it and what it can do:

  - Hook up market data to the marketDataService Observable
  - Aggregate tick data to 1-minute bars , using groupBy , flatmap and buffer operators


### 1. Hook up market data to the marketDataService Observable

    :::java
     public void subscribeRealTimeData(Instrument instrument) {
        controller.reqTopMktData(instrument.ibContract, "232", false, new ApiController.ITopMktDataHandler() 
        {
            @Override
            public void tickPrice(TickType tickType, double price, int canAutoExecute) {

                if (tickType == TickType.ASK) 
                {
                    log.info("IB tick " + new Date() + " price " + price);
                    LivePriceEvent priceEvent = new LivePriceEvent(System.currentTimeMillis(), instrument, new BigDecimal(price).setScale(3, RoundingMode.UP));
                    marketDataObservable.push(priceEvent);
                }

            }
            


Now each time a tick arrives from IB , it will be pushed to our Obseravble . Now we can now fold the data as we want using the different opearator of RxJava Observable

### 2. Aggregate tick data to 1-minute bars
    :::java
    public void aggregateLiveMinuteBar() {

        observable().
                ofType(LivePriceEvent.class). //filter on live ticks
                groupBy(LivePriceEvent::getInstrument). // group by instrument i.e AAPL, GOOG
                flatMap(grouped -> grouped.buffer(2, 1)). // take each 2 consecutive events
                subscribe(listOf2 -> {
                    LivePriceEvent lastEvent = listOf2.get(0);
                    int lastMinute = new DateTime(lastEvent.getCreateTimestamp()).minuteOfHour().get();
                    int currentMinute = new DateTime(listOf2.get(1).getCreateTimestamp()).minuteOfHour().get();
            //when minute is crossed , we push the result back in the observable to make it available to other subscribers
            if (lastMinute != currentMinute) {
                        push(new LiveBarEvent(TimeUnit.MINUTES, lastEvent.createTimestamp, lastEvent.getInstrument(), lastEvent.getPrice()));
                    }

        });


    }

### 3. Running the minute bar aggregator against IB demo feed
just follow the instructions from the [github](https://github.com/dsebban/blog-post-1)


```sh
$ git clone [https://github.com/dsebban/blog-post-1] rx-ib
$ cd rx-ib
$ mvn package
$ foreman start

```

you should see something like this 


```sh
daniel@daniel-desktop:~/Projects/dice_bot/blog-post-1$ foreman start

16:22:37 ib.1   | started with pid 29935
16:22:37 app.1  | started with pid 29937
16:22:47 app.1  | Server Version:76
16:22:47 app.1  | TWS Time at connection:20150717 16:22:44 IST
16:22:47 app.1  | Jul 17, 2015 4:22:47 PM daniels.reactive.blog.InteractiveBrokersFeed$2 connected
16:22:47 app.1  | INFO: connected
16:22:48 app.1  | Jul 17, 2015 4:22:48 PM daniels.reactive.blog.InteractiveBrokersFeed$2 message
16:22:48 app.1  | SEVERE: id -1 errocode = 2119msg Market data farm is connecting:ibdemo
16:22:48 app.1  | Jul 17, 2015 4:22:48 PM daniels.reactive.blog.InteractiveBrokersFeed$2 message
16:22:48 app.1  | SEVERE: id -1 errocode = 2104msg Market data farm connection is OK:ibdemo
16:22:48 app.1  | Jul 17, 2015 4:22:48 PM daniels.reactive.blog.InteractiveBrokersFeed$1 tickPrice
16:22:48 app.1  | INFO: IB tick Fri Jul 17 16:22:48 IDT 2015 price 122.09
16:22:48 app.1  | Jul 17, 2015 4:22:48 PM daniels.reactive.blog.InteractiveBrokersFeed$1 tickPrice
16:22:48 app.1  | INFO: IB tick Fri Jul 17 16:22:48 IDT 2015 price 122.08
16:22:52 app.1  | Jul 17, 2015 4:22:52 PM daniels.reactive.blog.InteractiveBrokersFeed$1 tickPrice
16:22:52 app.1  | INFO: IB tick Fri Jul 17 16:22:52 IDT 2015 price 122.09
16:22:58 app.1  | Jul 17, 2015 4:22:58 PM daniels.reactive.blog.InteractiveBrokersFeed$1 tickPrice
16:22:58 app.1  | INFO: IB tick Fri Jul 17 16:22:58 IDT 2015 price 122.08
16:23:00 app.1  | Jul 17, 2015 4:23:00 PM daniels.reactive.blog.InteractiveBrokersFeed$1 tickPrice
16:23:00 app.1  | INFO: IB tick Fri Jul 17 16:23:00 IDT 2015 price 122.09
16:23:00 app.1  | Jul 17, 2015 4:23:00 PM daniels.reactive.blog.Main lambda$main$0
16:23:00 app.1  | INFO: minute = 22 val=LiveBarEvent(barDuration=MINUTES, createTimestamp=1437139378855, instrument=APPL, price=122.080)
```


