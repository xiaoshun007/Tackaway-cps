<template>
<!--miniprogram/pages/user/user.wxml-->
<view class="user">
  <!-- 未登录时 -->
  <view class="logout" v-if="!logged">
    <text>请登录后查看您收藏的菜品</text>
    <button open-type="getUserInfo" @getuserinfo="onGetUserInfo" class="userinfo-avatar">
      登录
    </button>
  </view>
  <view class="login" v-if="logged">
    <view class="name">
      <image :src="avatarUrl"></image>
      <text>{{username}}</text>
      <text>{{place}}</text>
    </view>
    <view class="collection" v-if="collectList.length">
      <view class="my">我的菜谱</view>

      <view v-for="(item, index) in collectList" :key="index" class="box" :data-id="item.id" @tap="goDetail">
        <image :src="item.albums[0]"></image>
        <view class="right">
          <text class="title">{{item.title}}</text>
          <text>{{item.itro}}</text>
          <text class="see">查看更多>></text>
        </view>
      </view>
    </view>
    <view class="collection" v-if="!collectList.length" style="text-align:center;padding-top:50rpx;">
      <text style="color:#666;">您还没有收藏过菜品</text>
    </view>
  </view>
</view>
</template>

<script>
// miniprogram/pages/user/user.js
const app = getApp();

export default {
  data() {
    return {
      userInfo: {},
      avatarUrl: '',
      openid: '',
      logged: false,
      username: '',
      place: '',
      collectList: []
    };
  },

  components: {},
  props: {},

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    console.log('进入用户页检查是否登录:', this.logged);
    console.log('是否已授权：', uni.getStorageSync('isLogin'));
    console.log('是否已有用户openId：', app.globalData.openid);
    uni.showLoading({
      title: '正在加载...',
      mask: true
    }); // 获取用户信息

    uni.getSetting({
      success: res => {
        if (res.authSetting['scope.userInfo']) {
          console.log('已授权'); // 已经授权，可以直接调用 getUserInfo 获取头像昵称，不会弹框

          uni.getUserInfo({
            success: res => {
              this.$scope.setData({
                logged: true,
                avatarUrl: res.userInfo.avatarUrl,
                userInfo: res.userInfo,
                username: res.userInfo.nickName,
                place: res.userInfo.province + ', ' + res.userInfo.country
              });
            }
          });
        }

        uni.hideLoading();
      }
    }); // 是否存在用户的openId

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
    this.getcollect();
    console.log(0);
  },

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
  onShareAppMessage: function () {},
  methods: {
    goDetail(e) {
      uni.navigateTo({
        url: `/pages/detail/detail?id=${e.currentTarget.dataset.id}`
      });
    },

    onGetUserInfo: function (e) {
      if (!this.logged && e.detail.userInfo) {
        console.log(e);
        uni.setStorageSync('isLogin', 'isLogin');
        this.$scope.setData({
          logged: true,
          avatarUrl: e.detail.userInfo.avatarUrl,
          userInfo: e.detail.userInfo,
          username: e.detail.userInfo.nickName,
          place: e.detail.userInfo.province + ', ' + e.detail.userInfo.country
        });
      }
    },

    // 读取收藏列表
    getcollect() {
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
            this.$scope.setData({
              collectList: []
            });
          } else {
            // 如果已有收藏记录
            db.collection('collects').doc('collect' + this.openid).get().then(res => {
              console.log(res.data);
              this.$scope.setData({
                collectList: res.data.collectList
              });
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
    }

  }
};
</script>
<style>
/* miniprogram/pages/user/user.wxss */

.user {
  font-size: 28rpx;
}

.logout {
  text-align: center;
  padding: 160rpx 200rpx;
}

.logout button {
  margin-top: 100rpx;
  line-height: 80rpx;
  font: 28rpx;
  background: #ff6262;
  color: #fff;
}

.login {
  margin: 0;
}

.login .name image {
  height: 140rpx;
  width: 140rpx;
  border-radius: 50%;
  animation: avator linear 16s infinite normal;
}

@keyframes avator {
  0% {
    transform: rotate(0deg);
  }

  100% {
    transform: rotate(360deg);
  }
}

.login .name {
  background: linear-gradient(#f79642, #f5798d);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 30rpx;
}

.login .name text {
  padding-top: 20rpx;
  color: #fff;
}

.login .collection {
  padding: 50rpx 30rpx;
  background: #fff;
}
.login .collection .my {
  font-weight: bold;
  border-left: 3px solid #ff6262;
  padding-left: 14rpx;
}

.box {
  border: 1px solid #ddd;
  margin: 40rpx 0 0 0;
  padding: 20rpx 30rpx 20rpx 270rpx;
  font-size: 28rpx;
  height: 200rpx;
  overflow: hidden;
  position: relative;
  border-radius: 10rpx;
  box-shadow: 1px 1px 6rpx #ccc;
}

.box image {
  height: 200rpx;
  width: 220rpx;
  position: absolute;
  top: 20rpx;
  left: 10rpx;
  border-radius: 10rpx;
}

.box view {
  padding-top: 0rpx;
}

.box view text {
  display: block;
  overflow: hidden;
  white-space: nowrap;
  text-overflow: ellipsis;
  padding-bottom: 10rpx;
  color: #555;
  font-size: 24rpx;
}

.box view text.title {
  color: #333;
  font-weight: 600;
  font-size: 30rpx;
  padding-bottom: 16rpx;
}

.box view text.see {
  color: #ff6262;
  padding-top: 40rpx;
}

</style>