<template>
<view>
<!--miniprogram/pages/detail/detail.wxml-->
<view class="detail" v-if="isExit">
    <view class="banner">
      <image :src="detail.albums[0]"></image>
    </view>
    <view class="title">
      <text>{{detail.title}}</text>
      <view class="see"> <image src="/static/images/see.png" mode="widthFix"></image> {{detail.count}} 人浏览</view>
      <view class="tags">
        <text v-for="(item, index) in tags" :key="index">{{item}}</text>
      </view>
      <view class="intro">
        {{detail.intro}}
      </view>
    </view>
    <view class="ingredients">
      <text>主料</text> 
      <text v-for="(item, index) in ingredients" :key="index">{{item}}</text>
    </view>
    <view class="ingredients">
      <text>辅料</text>
      <text v-for="(item, index) in burden" :key="index">{{item}}</text>
    </view>
    <view class="steps"> 
      <text class="top">步骤</text>
      <view v-for="(item, index) in detail.steps" :key="index" class="item">
        <text>第{{index + 1}}步</text>
        <image :src="item.img"></image>
        <view>{{item.step}}</view>
      </view> 
    </view>
</view>

<!-- 首页 -->
<view class="backhome" @tap="onBackhome">
  <image src="/static/images/nav/index-active.png"></image>
  <!-- <text>首页</text> -->
</view>

<!-- 分享 -->
<view class="share">
  <image src="/static/images/share.png"></image>
  <text>分享</text>
  <button open-type="share"></button>
</view>

<!-- 用户未登录 -->
<!-- <view class="collect" v-if="!logged" style="z-index:11;background: rgba(0, 0, 0, .1);">
  <button open-type="getUserInfo" @getuserinfo="getUser" style="border:1;"></button>
</view> -->

<!-- 用户已登录 -->
<view class="collect" @tap.stop="bindCollect">
  <image src="/static/images/collect.png"></image>
  <text v-if="isCollect">收藏</text>
  <text v-if="!isCollect">已收藏</text>
</view>

<view class="no-list" v-if="!isExit" style="text-align:center;font-size:24rpx;padding:30rpx;">
  <text style="color:#666;">--- 未找到您搜索的菜品 ---</text>
</view>
</view>
</template>

<script>
// miniprogram/pages/detail/detail.js
const app = getApp();

export default {
  data() {
    return {
      detail: {},
      openid: '',
      tags: [],
      // 标签
      ingredients: [],
      // 主料
      burden: [],
      // 辅料
      loading: true,
      logged: false,
      isExit: true,
      // 此菜品是否存在
      isCollect: true // 菜品是否已收藏

    };
  },

  components: {},
  props: {},

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    let isLogin = uni.getStorageSync('isLogin');
    this.loadDetail(options.id); // 加载详情

    uni.setStorageSync('shareId', options.id);
    console.log(options.id);
    console.log('用户是否授权：', isLogin);
    console.log('是否已有用户openId：', app.globalData.openid);
    this.$scope.setData({
      logged: isLogin ? true : false
    }); // 是否存在用户的openId

    if (app.globalData.openid) {
      this.$scope.setData({
        openid: app.globalData.openid
      });
    }

    this.getcollect(options.id); // 获取收藏菜品，并判断是否已收藏 
  },

  /**
   * 生命周期函数--监听页面初次渲染完成
   */
  onReady: function () {},

  /**
   * 生命周期函数--监听页面显示
   */
  onShow: function () {},

  /**
   * 生命周期函数--监听页面隐藏
   */
  onHide: function () {},

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
  onShareAppMessage: function () {
    let id = uni.getStorageSync('shareId');
    return {
      title: '小菜一碟',
      path: `pages/detail/detail?id=${id}`
    };
  },
  methods: {
    loadDetail(param) {
      let that = this;
      uni.showLoading({
        title: '详情加载中...'
      }); // 从云数据库读取列表

      const db = uniCloud.database();
      const _ = db.command;
      console.log("param：", param);
      db.collection('foods').where({
        id: _.eq(param)
      }).get().then(res => {
          console.log('查询结果:', res.result.data);
          console.log(res.result.data.length);

          if (res.result.data.length) {
            console.log(12345);
            console.log("data:", res.result.data[0]);
            console.log(res.result.data[0].ingredients.split(',').join('：').split(';'));
            console.log(res.result.data[0].burden.split(',').join('：').split(';'));
            this.$scope.setData({
              detail: res.result.data[0],
              tags: res.result.data[0].category,
              ingredients: res.result.data[0].ingredients.split(',').join('：').split(';'),
              burden: res.result.data[0].burden.split(',').join('：').split(';')
            });
            console.log(111111);
            uni.setNavigationBarTitle({
              title: res.result.data[0].title
            });
          } else {
            console.log('该id为空');
            this.$scope.setData({
              isExit: false
            });
          }

          uni.hideLoading();
        });
    },

    // 登录授权
    getUser(e) {
      console.log(e);
      uni.getUserInfo({
        success: res => {
          console.log(res);
          uni.setStorageSync('isLogin', 'isLogin');
          this.$scope.setData({
            logged: true
          });
        }
      });
    },

    // 授权后可以收藏
    bindCollect() {
      let that = this; // 先检查是否以获取openId

      if (!this.openid) {
        wx.cloud.callFunction({
          name: 'login',
          data: {},
          success: res => {
            console.log('取到openId：', res.result);
            app.globalData.openid = res.result.openid;
            this.$scope.setData({
              openid: res.result.openid
            });
            that.onCollect();
            uni.vibrateLong({
              success: res => {
                console.log('震动成功');
              },
              fail: err => {
                console.log('震动失败');
              }
            });
            uni.showToast({
              icon: '收藏',
              title: '收藏成功'
            });
          },
          fail: err => {
            uni.showToast({
              icon: 'none',
              title: '获取 openid 失败，请检查是否有部署 login 云函数'
            });
            console.log('[云函数] [login] 获取 openid 失败，请检查是否有部署云函数，错误信息：', err);
          }
        });
      } else {
        that.onCollect();
        uni.vibrateLong({
          success: res => {
            console.log('震动成功');
          },
          fail: err => {
            console.log('震动失败');
          }
        });

        if (that.isCollect) {
          uni.showToast({
            icon: '收藏',
            title: '收藏成功'
          });
        } else {
          uni.showToast({
            icon: '收藏',
            title: '已经取消收藏'
          });
        }
      }
    },

    // 收藏
    onCollect() {
      const db = uniCloud.database();
      let that = this; // 查看是否有收藏记录

      db.collection('collects').where({
        _openid: this.openid,
        _id: 'collect' + this.openid
      }).get({
        success: res => {
          console.log('[数据库] [查询记录] 成功: ', res);
          let like = that.detail; // 需要收藏的菜品

          delete like._id;
          delete like._openid;

          if (!res.data.length) {
            // 如果从未收藏
            console.log(' 从未收藏');
            let detailArray = [];
            detailArray.push(like);
            db.collection('collects').add({
              data: {
                _id: 'collect' + that.openid,
                description: 'like',
                collectList: detailArray
              }
            }).then(res => {
              console.log(res);
            });
          } else {
            // 如果已有收藏记录
            console.log('已有收藏记录');
            let detailArray = res.data[0].collectList;
            let i = 0;
            let flag = false; // 判断已有的收藏记录中是否已经收藏了此菜品

            detailArray.map((val, index) => {
              if (val.id == like.id) {
                i = index;
                flag = true;
              }
            });
            this.$scope.setData({
              isCollect: flag
            });
            that.isCollect ? detailArray.splice(i, 1) : detailArray.push(like);
            db.collection('collects').doc('collect' + that.openid).update({
              data: {
                collectList: detailArray
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

    // 读取收藏列表
    getcollect(param) {
      let that = this;
      const db = uniCloud.database(); // 查看是否有收藏记录

      db.collection('collects').where({
        _openid: this.openid,
        _id: 'collect' + this.openid
      }).get({
        success: res => {
          console.log('[数据库] [查询记录] 成功: ', res);

          if (!res.data.length) {
            // 如果从未收藏
            console.log(' 从未收藏');
          } else {
            // 如果已有收藏记录
            console.log(res.data);
            let detailArray = res.data[0].collectList;
            let flag = false; // 判断已有的收藏记录中是否已经收藏了此菜品

            detailArray.map((val, index) => {
              if (val.id == param) {
                flag = true;
              }
            });
            console.log(flag);
            this.$scope.setData({
              isCollect: !flag
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

    // onShareAppMessage(res) {
    //   let id = wx.getStorageSync('shareId')
    //   if (res.from === 'button') {
    //     // 来自页面内转发按钮
    //     console.log(res.target)
    //   }
    //   return {
    //     title: '小菜一碟',
    //     path: `pages/detail/detail?id=${id}`
    //   }
    // },
    onBackhome() {
      uni.switchTab({
        url: `/pages/index/index`
      });
    }

  }
};
</script>
<style>
/* miniprogram/pages/detail/detail.wxss */
page {
  background: #e7e8e7;
}
.detail {
  font-size: 28rpx; 
}
.detail .banner {
  height: 500rpx;
  overflow: hidden;
}
.detail .banner image {
  width: 100%;
  height: 100%;
}
.title {
  background: #fff;
  text-align: center;
  padding: 40rpx 30rpx; 
}

.title>text:nth-child(1) {
  font-size: 34rpx;
  margin-bottom: 20rpx;
  display: block;
  color: #444;
}
.title .tags text {
  display: inline-block;
  border: 1px solid #ddd;
  color: #777;
  margin: 10rpx;
  padding: 4rpx 20rpx;
  border-radius: 30rpx;
  font-size: 24rpx;
}
.title .see {
  font-size: 24rpx;
  color: #777;
  padding-bottom: 20rpx;
  display: flex;
  align-items: center;
  justify-content: center;
}
.title .see image {
  width: 30rpx; 
  margin-right: 10rpx;
}
.title .intro {
  font-size: 24rpx;
  color: #666;
  padding-top: 30rpx;
}

.ingredients {
  margin-top: 20rpx;
  padding: 20rpx 30rpx;
  display: flex;
  flex-direction: column;
  background: #fff;
}
.ingredients text:nth-child(1) {
  font-size: 36rpx;
  font-weight: bold;
  text-align: center;
  padding: 20rpx;
}

.ingredients text:not(:first-child)  {
  font-size: 28rpx;
  padding: 10rpx 0;
  color: #666;
}

.steps {
  margin-top: 20rpx;
  padding: 20rpx 30rpx;
  background: #fff;
}
.steps .top {
  font-size: 36rpx;
  font-weight: bold;
  text-align: center;
  display: block;
  padding: 20rpx;
}

.steps .item {
  padding: 30rpx 0;
  text-align: center;
}
.steps .item text {
  font-size: 32rpx;
  color: #FF6262;
  padding: 0 20rpx;
  margin-bottom: 20rpx;
  border-left: 8rpx solid #FF6262;
  display: block;
  text-align: left;
}

.steps .item view {
  font-size: 28rpx;
  color: #444;
  padding: 20rpx 0; 
}

.collect { 
  height: 120rpx;
  width: 120rpx;
  position: fixed;
  bottom: 30rpx;
  right: 30rpx;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  font-size: 24rpx;
  background: rgba(0, 0, 0, .6);
  border-radius: 50%;
  z-index: 10;
}

.collect image {
  height: 50rpx;
  width: 50rpx;
}
.collect text {
  color: #fff;  
}

.collect button {
  position: absolute;
  height: 100%;
  width: 100%;
  opacity: 0.1;
}


.share { 
  height: 120rpx;
  width: 120rpx;
  position: fixed;
  bottom: 170rpx;
  right: 30rpx;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  font-size: 24rpx;
  background: rgba(0, 0, 0, .6);
  border-radius: 50%;
  z-index: 10;
} 
.share image {
  height: 70rpx;
  width: 70rpx;
}
.share text {
  color: #fff;  
}

.share button {
  position: absolute;
  height: 100%;
  width: 100%;
  opacity: 0.1;
  z-index: 99;
}

.backhome { 
  height: 100rpx;
  width: 100rpx;
  position: fixed;
  top: 10rpx;
  right: 20rpx;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  font-size: 24rpx;
  background: rgba(255, 255, 255, .4);
  border-radius: 50%;
  z-index: 10;
} 
.backhome image {
  height: 60rpx;
  width: 60rpx;
}
.backhome text {
  color: #fff;  
}



</style>