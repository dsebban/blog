Title: RxJava in Action with Interactive Brokers market data
Date: 2010-12-03 10:20
Category: Java 

In one of my recent projects I automated a trading strategy using [Iteractive Brokers](https://www.interactivebrokers.com/en/?f=%2Fen%2Fsoftware%2Fibapi.php&ns=T) Java API,
 the perfect fit to handle the live and historical data and produce metrics or pass order is
[RxJava](https://github.com/ReactiveX/RxJava)  . Reading the doc and example of RXJava can be intimidating and quite abstract , here is a hands on example of how to use it and what it can do:

  - Hook up market data to the marketDataService Observable
  - Aggregate tick data to 1-minute bars
  - Calculate moving average for AAPL
  - Pass a buy order when moving avg below a given threshold



### 1. Hook up market data to the marketDataService Observable

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

### 2. Aggregate tick data to 1-minute bars
    :::java
    private void aggregateRealTime(RealTimeTickEvent e , Func1<RealTimeTickEvent,Map<Instrument, LinkedList<RealTimeTickEvent>>> mapFactory, Func2<RealTimeTickEvent,BigDecimal,HistoricalBarEvent> tickfactory){

        LinkedList<RealTimeTickEvent> ticks = mapFactory.call(e).get(e.getInstrument());

        if(ticks ==null){
            ticks = new LinkedList<RealTimeTickEvent>();
            mapFactory.call(e).put(e.getInstrument(),ticks);
        }

        if (ticks.size() > 0) {
            int lastMinute = new DateTime(ticks.getFirst().getCreateTimestamp()).minuteOfHour().get();
            int currentMinute = new DateTime(e.getCreateTimestamp()).minuteOfHour().get();

            if (lastMinute != currentMinute) {
                BigDecimal avg = ticks.stream().map(RealTimeTickEvent::getPrice).reduce(BigDecimal::add).get().divide(new BigDecimal(ticks.size()),3,BigDecimal.ROUND_UP);
                HistoricalBarEvent bar = tickfactory.call(ticks.getFirst(),avg);
                ticks.clear();
                push(bar);

            }
        }
        ticks.push(e);
    }

### 3. Calculate moving average for AAPL


### 4. Pass a buy order when moving avg below a given threshold














Markdown is a lightweight markup language based on the formatting conventions that people naturally use in email.  As [John Gruber] writes on the [Markdown site] [1]:

> The overriding design goal for Markdown's
> formatting syntax is to make it as readable
> as possible. The idea is that a
> Markdown-formatted document should be
> publishable as-is, as plain text, without
> looking like it's been marked up with tags
> or formatting instructions.

This text you see here is *actually* written in Markdown! To get a feel for Markdown's syntax, type some text into the left window and watch the results in the right.

### Version
3.0.0

### Tech

Dillinger uses a number of open source projects to work properly:

* [AngularJS] - HTML enhanced for web apps!
* [Ace Editor] - awesome web-based text editor
* [Marked] - a super fast port of Markdown to JavaScript
* [Twitter Bootstrap] - great UI boilerplate for modern web apps
* [node.js] - evented I/O for the backend
* [Express] - fast node.js network app framework [@tjholowaychuk]
* [Gulp] - the streaming build system
* [keymaster.js] - awesome keyboard handler lib by [@thomasfuchs]
* [jQuery] - duh

### Installation

```sh
$ git clone [git-repo-url] dillinger
$ cd dillinger
$ npm i -d
$ mkdir -p public/files/{md,html,pdf}
$ gulp build --prod
$ NODE_ENV=production node app
```

### Plugins

Dillinger is currently extended with the following plugins

* Dropbox
* Github
* Google Drive
* OneDrive

Readmes, how to use them in your own application can be found here:

* plugins/dropbox/README.md
* plugins/github/README.md
* plugins/googledrive/README.md
* plugins/onedrive/README.md

### Development

Want to contribute? Great!

Dillinger uses Gulp + Webpack for fast developing.
Make a change in your file and instantanously see your updates!

Open your favorite Terminal and run these commands.

First Tab:
```sh
$ node app
```

Second Tab:
```sh
$ gulp watch
```

(optional) Third:
```sh
$ karma start
```

### Todo's

Write Tests
Github saving overhaul
Code Commenting
Night Mode

License
----

MIT


**Free Software, Hell Yeah!**

[john gruber]:http://daringfireball.net/
[@thomasfuchs]:http://twitter.com/thomasfuchs
[1]:http://daringfireball.net/projects/markdown/
[marked]:https://github.com/chjj/marked
[Ace Editor]:http://ace.ajax.org
[node.js]:http://nodejs.org
[Twitter Bootstrap]:http://twitter.github.com/bootstrap/
[keymaster.js]:https://github.com/madrobby/keymaster
[jQuery]:http://jquery.com
[@tjholowaychuk]:http://twitter.com/tjholowaychuk
[express]:http://expressjs.com
[AngularJS]:http://angularjs.org
[Gulp]:http://gulpjs.com
