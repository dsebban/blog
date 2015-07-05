Title: Java Rx with live financial market data from IB 
Date: 2010-12-03 10:20
Category: Java 

In this blog post I will talk about the perfect match Java Rx and live financial data , I will show how to abstract Interactive Brokers market data feed with a Java Rx Observable class , this will allow us to o some pretty cool stuff with the live data liek calculate live metrics.

First let s hookup IB market data feed with our marketDataService (our Rx Observables)

    :::java
     public void subscribeRealTimeData(Instrument instrument) {
        controller.reqTopMktData(instrument.ibContract, "232", false, new ApiController.ITopMktDataHandler() {
            @Override
            public void tickPrice(TickType tickType, double price, int canAutoExecute) {
                if(tickType == TickType.BID) {
                    RealTimeBidTickEvent tick = new RealTimeBidTickEvent(System.currentTimeMillis(),  instrument, new BigDecimal(price).setScale(3, RoundingMode.UP));
                    marketDataService.onNext(tick);
                }
                if(tickType == TickType.ASK) {
                    RealTimeAskTickEvent tick = new RealTimeAskTickEvent(System.currentTimeMillis(),  instrument, new BigDecimal(price).setScale(3, RoundingMode.UP));
                    marketDataService.onNext(tick);
                }
            }

Now each time a tick arrives from IB , it will be pushed to our Obseravble , let''s have some fun and and start by aggregating our tick data into a minute data bar.




