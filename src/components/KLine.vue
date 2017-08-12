<template>
  <div class="kline" id="kline">
  </div>
</template>

<script>
import echarts from 'echarts'


var option = {
    backgroundColor: '#21202D',
    legend: {
        data: ['日K', 'MA5', 'MA10', 'MA20', 'MA30'],
        inactiveColor: '#777',
        textStyle: {
            color: '#fff'
        }
    },
    tooltip: {
        trigger: 'axis',
        axisPointer: {
            animation: false,
            type: 'cross',
            lineStyle: {
                color: '#376df4',
                width: 2,
                opacity: 1
            }
        }
    },
    xAxis: {
        type: 'category',
        axisLine: { lineStyle: { color: '#8392A5' } }
    },
    yAxis: {
        scale: true,
        axisLine: { lineStyle: { color: '#8392A5' } },
        splitLine: { show: false }
    },
    grid: {
        bottom: 80
    },
    dataZoom: [{
      textStyle: {
          color: '#8392A5'
      },
      handleIcon: 'M10.7,11.9v-1.3H9.3v1.3c-4.9,0.3-8.8,4.4-8.8,9.4c0,5,3.9,9.1,8.8,9.4v1.3h1.3v-1.3c4.9-0.3,8.8-4.4,8.8-9.4C19.5,16.3,15.6,12.2,10.7,11.9z M13.3,24.4H6.7V23h6.6V24.4z M13.3,19.6H6.7v-1.4h6.6V19.6z',
      handleSize: '80%',
      dataBackground: {
          areaStyle: {
              color: '#8392A5'
          },
          lineStyle: {
              opacity: 0.8,
              color: '#8392A5'
          }
      },
      handleStyle: {
          color: '#fff',
          shadowBlur: 3,
          shadowColor: 'rgba(0, 0, 0, 0.6)',
          shadowOffsetX: 2,
          shadowOffsetY: 2
      }
    }, {
        type: 'inside'
    }],
    animation: false,
    calculable: false,
    addDataAnimation: false,
    animationThreshold: false,
    series: [
        {
            type: 'candlestick',
            name: '日K',
            itemStyle: {
                normal: {
                    color: '#FD1050',
                    color0: '#0CF49B',
                    borderColor: '#FD1050',
                    borderColor0: '#0CF49B'
                }
            }
        },
        {
            name: 'MA5',
            type: 'line',
            smooth: true,
            showSymbol: false,
            lineStyle: {
                normal: {
                    width: 1
                }
            }
        },
        {
            name: 'MA10',
            type: 'line',
            smooth: true,
            showSymbol: false,
            lineStyle: {
                normal: {
                    width: 1
                }
            }
        },
        {
            name: 'MA20',
            type: 'line',
            smooth: true,
            showSymbol: false,
            lineStyle: {
                normal: {
                    width: 1
                }
            }
        },
        {
            name: 'MA30',
            type: 'line',
            smooth: true,
            showSymbol: false,
            lineStyle: {
                normal: {
                    width: 1
                }
            }
        },
        {
            name: 'MACD',
            type: 'line',
            smooth: true,
            showSymbol: false,
            lineStyle: {
                normal: {
                    width: 1
                }
            }
        }
    ]
};

var timestamp = "";

export default {
  name: 'kline',
  data () {
    return {
      dates: [],
      data: [],
      msg: 'Welcome to K Line',
      ws: new WebSocket('ws://' + "127.0.0.1:8000/feed")
    }
  },
  mounted() {
      this.$nextTick(function() {
          this.todo()
      })
  },
  methods: {
    todo() {
      this.chart = echarts.init(document.getElementById('kline'));
      setInterval(this.draw, 3000);
    },
    draw() {
      var dataset = [], dates=[];
      var that = this;
      this.ws.onmessage = function(event) {
        var data = JSON.parse(event.data);
        that.dataset = data.dataset;
        that.dates = data.dates;
        };
      timestamp = this.dates[this.dates.length - 1] || ""
      this.ws.send(timestamp)
      option.xAxis.data = that.dates;
      option.series[0].data = that.dataset;
      option.series[1].data = this.calculateMA(5, that.dataset);
      option.series[2].data = this.calculateMA(10, that.dataset);
      option.series[3].data = this.calculateMA(20, that.dataset);
      option.series[4].data = this.calculateMA(30, that.dataset);
      option.series[5].data = this.calculateMACD(that.dataset);
      this.chart.setOption(option);
    },
    calculateMA(dayCount, data) {
      var result = [];
      for (var i = 0, len = data.length; i < len; i++) {
          if (i < dayCount) {
              result.push('-');
              continue;
          }
          var sum = 0;
          for (var j = 0; j < dayCount; j++) {
              sum += data[i - j][1];
          }
          result.push(sum / dayCount);
      }
      return result;
    },
    calculateMACD(data) {
      var length = data.length;
      var ema12 = new Array(length), ema26 = new Array(length), dif = new Array(length), dea = new Array(length);
      for (var i = 0; i < length; i++) {
        ema12[i] = ema12[i-1]*11/13 + data[i][2]*2/13;
        ema26[i] = ema26[i-1]*25/27 + data[i][2]*2/27;
        dif[i] = ema12[i] - ema26[i];
        dea[i] = dea[i-1]*8/10 + dif[i]*2/10;
      }
      return dif;
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
#kline {
    /*需要制定具体高度，以px为单位*/
    height: 900px;
  }
</style>
