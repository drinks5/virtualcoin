<template>
  <div class="kline">
    <h1>{{ msg }}</h1>
    <div id='kline'></div>
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
    animation: true,
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
        }
    ]
};
export default {
  name: 'kline',
  data () {
    return {
      dates: [],
      data: [],
      msg: 'Welcome to K Line'
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
        this.intervalid1 = setInterval(this.draw, 1000);
    },
    draw() {
      option.xAxis.data = this.dates;
      option.series[0].data = this.calculateMA(5, this.data);
      option.series[1].data = this.calculateMA(10, this.data);
      option.series[2].data = this.calculateMA(20, this.data);
      option.series[3].data = this.calculateMA(30, this.data);
      this.chart.showLoading();
      this.chart.setOption(option);
      this.chart.hideLoading();
    },
    calculateMA(dayCount) {
      var result = [];
      for (var i = 0, len = this.data.length; i < len; i++) {
          if (i < dayCount) {
              result.push('-');
              continue;
          }
          var sum = 0;
          for (var j = 0; j < dayCount; j++) {
              sum += this.data[i - j][1];
          }
          result.push(sum / dayCount);
      }
      return result;
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
#kline {
    /*需要制定具体高度，以px为单位*/
    height: 400px;
  }  
</style>
