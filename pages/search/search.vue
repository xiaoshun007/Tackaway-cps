<template>
<view>
  <view class="search">
    <image src="/static/images/search.png"></image>
    <input placeholder="今天吃什么" focus @input="bindKeyInput" @confirm="goSearch">
    <text @tap="goSearch">搜索</text>
  </view>
  <view class="history">
    <text class="title">搜索历史</text>
    <text class="clear" v-if="historyList.length" @tap="bindClearHistory">清空历史</text>
    <view>
      <text v-for="(item, index) in historyList" :key="index" @tap="historyGoSearch" :data-title="item">{{item}}</text>
    </view>
  </view>

    <view v-if="!historyList.length" style="text-align:center;color:#666;font-size:24rpx;">
      搜索历史为空
    </view>
</view>
</template>

<script>
// miniprogram/pages/search/search.js
const app = getApp();

export default {
  data() {
    return {
      inputValue: '',
      openid: '',
      showHistory: true,
      historyList: []
    };
  },

  components: {},
  props: {},

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    console.log('是否已有用户openId：', app.globalData.openid); // 是否存在用户的openId

    if (app.globalData.openid) {
      this.$scope.setData({
        openid: app.globalData.openid
      });
    }
  },

  /**
   * 生命周期函数--监听页面初次渲染完成
   */
  onReady: function () {},

  /**
   * 生命周期函数--监听页面显示
   */
  onShow: function () {
    this.getHistory();
  },

  /**
   * 生命周期函数--监听页面隐藏
   */
  onHide: function () {
    this.getHistory();
  },

  /**
   * 生命周期函数--监听页面卸载
   */
  onUnload: function () {},

  /**
   * 页面相关事件处理函数--监听用户下拉动作
   */
  onPullDownRefresh: function () {},

  /**
   * 页面上拉触底事件的处理函数
   */
  onReachBottom: function () {},

  /**
   * 用户点击右上角分享
   */
  onShareAppMessage: function () {},
  methods: {
    bindKeyInput(e) {
      this.$scope.setData({
        inputValue: e.detail.value
      });
	  console.log(e)
      console.log("input：", this.inputValue);
    },

    // 进入搜索结果页 -> list
    goSearch() {
      let content = this.inputValue;

      if (!content) {
        console.log('内容为空');
        return;
      }

      this.onHistory(content);
      uni.navigateTo({
        url: `/pages/list/list?content=${content}`
      });
    },

    historyGoSearch(e) {
      console.log(e);
      let content = e.currentTarget.dataset.title;
      uni.navigateTo({
        url: `/pages/list/list?content=${content}`
      });
    },

    // 清空历史记录
    bindClearHistory() {
      const db = uniCloud.database();
      db.collection('historys').doc('history' + this.openid).update({
        data: {
          historyList: []
        }
      }).then(res => {
        console.log(res);
        uni.showToast({
          icon: '删除',
          title: '清空历史'
        });
      });
      this.$scope.setData({
        historyList: []
      });
    },

    // 添加历史记录
    onHistory(content) {
      const db = uniCloud.database();
      let that = this; // 查看是否有历史记录

      db.collection('historys').where({
        _openid: this.openid,
        _id: 'history' + this.openid
      }).get({
        success: res => {
          console.log('[数据库] [查询记录] 成功: ', res);

          if (!res.data.length) {
            console.log(' 历史记录为空');
            let historyArray = [];
            historyArray.unshift(content);
            db.collection('historys').add({
              data: {
                _id: 'history' + that.openid,
                description: 'history',
                historyList: historyArray
              }
            }).then(res => {
              console.log(res);
            });
          } else {
            console.log('已有历史记录');
            let historyArray = res.data[0].historyList;
            historyArray.unshift(content);
            console.log([...new Set(historyArray)]);
            db.collection('historys').doc('history' + that.openid).update({
              data: {
                historyList: [...new Set(historyArray)]
              }
            }).then(res => {
              console.log(res);
            });
          }
        },
        fail: err => {
          uni.showToast({
            icon: 'none',
            title: '查询记录失败'
          });
          console.error('[数据库] [查询记录] 失败：', err);
        }
      });
    },

    // 读取历史记录
    getHistory() {
      let that = this;
      const db = uniCloud.database();
      db.collection('historys').doc('history' + that.openid).get({
        success(res) {
          console.log(res.data);
          this.$scope.setData({
            historyList: res.data.historyList
          });
        }

      });
    }

  }
};
</script>
<style>
/* miniprogram/pages/search/search.wxss */

.search {
  margin: 20rpx;
  box-sizing: border-box;
  border-radius: 50rpx;
  height: 80rpx;
  padding: 0 0 0 20rpx;
  background: #fff;
  display: flex;
  align-items: center;
  justify-content: flex-start;
  font-size: 28rpx;
  border: 1px solid rgba(255, 98, 98, .7);
}

.search image {
  height: 36rpx;
  width: 36rpx;
  margin-right: 20rpx;
}

input {
  border: none;
  flex: 1;
}

.search text {
  padding: 20rpx 40rpx 20rpx 30rpx;
  background: #ff6262;
  color: #fff;
  border-top-right-radius: 50rpx;
  border-bottom-right-radius: 50rpx;
}

.history {
  margin-top: 30rpx;
  font-size: 28rpx;
  padding: 30rpx;
  color: #555;
  position: relative;
}

.history view {
  margin-top: 40rpx;
  display: flex;
  flex-wrap: wrap;
}

.history .title {
  color: #ff6262;
}

.history view text {
  border: 1px solid #ddd;
  padding: 8rpx 50rpx;
  border-radius: 40rpx;
  margin: 20rpx 30rpx 20rpx 0;
}

.clear {
  color: #888;
  position: absolute;
  right: 30rpx;
  top: 30rpx;
}

</style>