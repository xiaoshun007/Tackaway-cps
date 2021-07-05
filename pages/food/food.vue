<template>
<!--index.wxml-->
<view class="container"> 
  <view class="top">
    <text> </text>
    <view class="search" @tap="goSearch">
      <image src="/static/images/search.png"></image>
      <input placeholder="今天吃什么" disabled>
    </view>
    
  </view>
  <swiper class="swiper" :indicator-dots="indicatorDots" :indicator-color="indicatorColor" :autoplay="autoplay" :interval="interval" :duration="duration">
    <block v-for="(item, index) in imgUrls" :key="index">
      <swiper-item>
        <image :src="item.url" :data-id="item.id" @tap="goDetail" class="slide-image"></image>
      </swiper-item>
    </block>
  </swiper>
  <view class="category">
    <view v-for="(item, index) in category" :key="index" :data-tags="item.id" :data-content="item.name" @tap="goList">
      <image :src="item.img" mode="aspectFit"></image>
      <text>{{item.name}}</text>
    </view>
  </view>
  <view class="place block">
    <view class="title">
      <text>热门标签</text>
      <text class="more" @tap="goMenu">查看更多 >> </text>
    </view>
    <scroll-view class="scroll-view" scroll-x>
      <view v-for="(item, index) in scroll" :key="index" :id="item.id" :data-tags="item.id" :data-content="item.name" @tap="goList">
        <image :src="item.img"></image>
        <text>{{item.name}}</text>
      </view>
    </scroll-view>
  </view>
  <view class="like block">
    <view class="title">
      <text>猜你喜欢</text>
      <text class="more">您喜欢的美食 </text>
    </view>
    <view class="list">
      <view v-for="(item, index) in list" :key="index" class="box" :data-tags="item.id" :data-id="item.id" :data-content="item.name" @tap="goList">
        <image :src="item.img"></image>
        <view class="tip">
          <text>{{item.name}}</text> 
        </view>
      </view>
    </view>
  </view>
</view>
</template>

<script>
//index.js
const app = getApp();

export default {
  data() {
    return {
      imgUrls: [{
        id: 10222,
        url: "/static/images/banner5.jpg"
      }, {
        id: 1,
        url: "/static/images/banner.jpg"
      }],
      indicatorDots: true,
      autoplay: true,
      indicatorColor: '#fedb00',
      interval: 2000,
      duration: 400,
      activeCategoryId: 1,
      category: [{
        id: "37",
        parentId: "1005",
        img: "/static/images/wu.png",
        name: '早餐'
      }, {
        id: "38",
        parentId: "1005",
        img: "/static/images/zao.png",
        name: '午餐'
      }, {
        id: "39",
        parentId: "1005",
        img: "/static/images/xiawu.png",
        name: '下午茶'
      }, {
        id: "40",
        parentId: "1005",
        img: "/static/images/wan.png",
        name: '晚餐'
      }, {
        id: "41",
        parentId: "1005",
        img: "/static/images/ye.png",
        name: '夜宵'
      }],
      scroll: [{
        id: 1,
        parentId: "10001",
        img: "/static/images/jiachangcai.jpg",
        name: '家常菜'
      }, {
        id: 2,
        parentId: "10001",
        img: "/static/images/kuaishouc.jpg",
        name: '快手菜'
      }, {
        id: 3,
        parentId: "10001",
        img: "/static/images/chuangyicai.jpg",
        name: '创意菜'
      }, {
        id: 4,
        parentId: "10001",
        img: "/static/images/sucai.jpg",
        name: '素菜'
      }, {
        id: 5,
        parentId: "10001",
        img: "/static/images/liangcai.jpg",
        name: '凉菜'
      }],
      list: [{
        id: 31,
        parentId: "10004",
        img: "/static/images/like/yangwei.jpg",
        name: '养胃',
        detail: {
          banner: '',
          title: ''
        }
      }, {
        id: 35,
        parentId: "10004",
        img: "/static/images/like/bugai.jpg",
        name: '美容',
        detail: {
          banner: '',
          title: ''
        }
      }, {
        id: 33,
        parentId: "10004",
        img: "/static/images/like/paidu.jpg",
        name: '明目',
        detail: {
          banner: '',
          title: ''
        }
      }, {
        id: 28,
        parentId: "10004",
        img: "/static/images/like/qingfei.jpg",
        name: '清热去火',
        detail: {
          banner: '',
          title: ''
        }
      }, {
        id: 29,
        parentId: "10004",
        img: "/static/images/like/hugan.jpg",
        name: '增肥',
        detail: {
          banner: '',
          title: ''
        }
      }, {
        id: 30,
        parentId: "10004",
        img: "/static/images/like/jianfei.jpg",
        name: '减肥',
        detail: {
          banner: '',
          title: ''
        }
      }],
      avatarUrl: "/static/pages/index/user-unlogin.png",
      userInfo: {},
      logged: false,
      takeSession: false,
      requestResult: ''
    };
  },

  components: {},
  props: {},
  onLoad: function () {
    if (!wx.cloud) {
      uni.redirectTo({
        url: '../chooseLib/chooseLib'
      });
      return;
    } // 获取用户信息


    uni.getSetting({
      success: res => {
        if (res.authSetting['scope.userInfo']) {
          // 已经授权，可以直接调用 getUserInfo 获取头像昵称，不会弹框
          uni.getUserInfo({
            success: res => {
              this.$scope.setData({
                avatarUrl: res.userInfo.avatarUrl,
                userInfo: res.userInfo
              });
            }
          });
        }
      }
    }); // 获取用户openId

    this.onGetOpenid();
  },

  onShareAppMessage(res) {
    return {
      title: '小菜一碟',
      path: `pages/index/index`
    };
  },

  methods: {
    goSearch(e) {
      uni.navigateTo({
        url: `/pages/search/search`
      });
    },

    goDetail(e) {
      uni.navigateTo({
        url: `/pages/detail/detail?id=${e.currentTarget.dataset.id}`
      });
    },

    goList(e) {
      console.log(e);
      uni.navigateTo({
        url: `/pages/list/list?content=${e.currentTarget.dataset.content}&tags=${e.currentTarget.dataset.tags}`
      });
    },

    goMenu(e) {
      uni.switchTab({
        url: `/pages/menu/menu`
      });
    },

    onGetUserInfo: function (e) {
      if (!this.logged && e.detail.userInfo) {
        this.$scope.setData({
          logged: true,
          avatarUrl: e.detail.userInfo.avatarUrl,
          userInfo: e.detail.userInfo
        });
      }
    },
    onGetOpenid: function () {
      // 调用云函数
      wx.cloud.callFunction({
        name: 'login',
        data: {},
        success: res => {
          console.log('[云函数] [login] user openid: ', res.result.openid);
          app.globalData.openid = res.result.openid;
        },
        fail: err => {
          console.error('[云函数] [login] 调用失败', err);
          uni.showToast({
            icon: 'none',
            title: '获取 openid 失败，请检查是否有部署 login 云函数'
          });
        }
      });
    },
    // 上传图片
    doUpload: function () {
      // 选择图片
      uni.chooseImage({
        count: 1,
        sizeType: ['compressed'],
        sourceType: ['album', 'camera'],
        success: function (res) {
          uni.showLoading({
            title: '上传中'
          });
          const filePath = res.tempFilePaths[0]; // 上传图片

          const cloudPath = 'my-image' + filePath.match(/\.[^.]+?$/)[0];
          wx.cloud.uploadFile({
            cloudPath,
            filePath,
            success: res => {
              console.log('[上传文件] 成功：', res);
              app.globalData.fileID = res.fileID;
              app.globalData.cloudPath = cloudPath;
              app.globalData.imagePath = filePath;
              uni.navigateTo({
                url: '../storageConsole/storageConsole'
              });
            },
            fail: e => {
              console.error('[上传文件] 失败：', e);
              uni.showToast({
                icon: 'none',
                title: '上传失败'
              });
            },
            complete: () => {
              uni.hideLoading();
            }
          });
        },
        fail: e => {
          console.error(e);
        }
      });
    }
  }
};
</script>
<style>
/**index.wxss**/

page {
  background: #f6f6f6;
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
}

.userinfo, .uploader, .tunnel {
  margin-top: 40rpx;
  height: 140rpx;
  width: 100%;
  background: #fff;
  border: 1px solid rgba(0, 0, 0, 0.1);
  border-left: none;
  border-right: none;
  display: flex;
  flex-direction: row;
  align-items: center;
  transition: all 300ms ease;
}

.userinfo-avatar {
  width: 100rpx;
  height: 100rpx;
  margin: 20rpx;
  border-radius: 50%;
  background-size: cover;
  background-color: white;
}

.userinfo-avatar:after {
  border: none;
}

.userinfo-nickname {
  font-size: 32rpx;
  color: #007aff;
  background-color: white;
  background-size: cover;
}

.userinfo-nickname::after {
  border: none;
}

.uploader, .tunnel {
  height: auto;
  padding: 0 0 0 40rpx;
  flex-direction: column;
  align-items: flex-start;
  box-sizing: border-box;
}

.uploader-text, .tunnel-text {
  width: 100%;
  line-height: 52px;
  font-size: 34rpx;
  color: #007aff;
}

.uploader-container {
  width: 100%;
  height: 400rpx;
  padding: 20rpx 20rpx 20rpx 0;
  display: flex;
  align-content: center;
  justify-content: center;
  box-sizing: border-box;
  border-top: 1px solid rgba(0, 0, 0, 0.1);
}

.uploader-image {
  width: 100%;
  height: 360rpx;
}

.tunnel {
  padding: 0 0 0 40rpx;
}

.tunnel-text {
  position: relative;
  color: #222;
  display: flex;
  flex-direction: row;
  align-content: center;
  justify-content: space-between;
  box-sizing: border-box;
  border-top: 1px solid rgba(0, 0, 0, 0.1);
}

.tunnel-text:first-child {
  border-top: none;
}

.tunnel-switch {
  position: absolute;
  right: 20rpx;
  top: -2rpx;
}

.disable {
  color: #888;
}

.service {
  position: fixed;
  right: 40rpx;
  bottom: 40rpx;
  width: 140rpx;
  height: 140rpx;
  border-radius: 50%;
  background: linear-gradient(#007aff, #0063ce);
  box-shadow: 0 5px 10px rgba(0, 0, 0, 0.3);
  display: flex;
  align-content: center;
  justify-content: center;
  transition: all 300ms ease;
}

.service-button {
  position: absolute;
  top: 40rpx;
}

.service:active {
  box-shadow: none;
}

.request-text {
  padding: 20rpx 0;
  font-size: 24rpx;
  line-height: 36rpx;
  word-break: break-all;
}

.top {
  background: #FF6262;
  height: 300rpx;
  position: relative;
  padding: 10rpx 20rpx;
}

.top .user {
  width: 50rpx;
  height: 60rpx;
  position: absolute;
  top: 10rpx;
  right: 10rpx;
}

.top text {
  display: block;
  text-align: center;
  height: 40rpx;
  font-style: oblique;
  font-weight: bold;
  letter-spacing: 2rpx;
}

.top .search {
  border: 1px solid fff;
  box-sizing: border-box;
  border-radius: 30rpx; 
  height: 60rpx;
  padding: 0 20rpx;
  background: #fff;
  display: flex;
  align-items: center;
  justify-content: flex-start;
  font-size: 28rpx;

}
.top .search image {
  height: 36rpx;
  width: 36rpx;
  margin-right: 20rpx;
}
.top input {
  border: none; 
  flex: 1;
}

swiper {
  height: 240rpx;
  margin: 0 30rpx; 
  position: relative;
  transform: translate(0, -160rpx);
  margin-bottom: -160rpx;
  overflow: hidden;
  border-radius: 20rpx;
  border: 1px solid #fae4e6;
  background: #FF6262;
}

.slide-image {
  width: 100%;
  height: 240rpx;
  border-radius: 20rpx;
}

.category {
  width: 100%;
  padding: 36rpx 0;
  display: flex;
  align-items: center;
  justify-content: space-around;
}

.category view {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: space-around;
  padding:10rpx 24rpx;
}

.category image {
  height: 60rpx;
  width: 60rpx;
}

.category text {
  font-size: 28rpx;
  color: #666;
}

/* 热门标签 */

.place {
  padding: 12rpx 0;
  width: 100%;
  height: 280rpx;
  overflow: hidden;
}

.block .title {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 18rpx;
}

.block .title text {
  font-size: 40rpx;
  font-weight: bold;
}

.block .title .more {
  font-size: 28rpx;
  font-weight: 400;
  color: #666;
}

.scroll-view {
  width: 100%;
  height: 240rpx; 
  white-space: nowrap; /* 规定段落中的文本不进行换行 */
}

.scroll-view view {
  width: 180rpx;
  height: 180rpx;
  padding: 0 16rpx;
  box-sizing: content-box;
  display: inline-block; /* 设置行内块元素 */
  position: relative;
}

.scroll-view view image {
  width: 180rpx;
  height: 180rpx;
  border-radius: 10rpx;
  opacity: 0.9;
}

.scroll-view view text {
  font-size: 24rpx;
  font-weight: bold;
  color: #fff;
  position: absolute; 
  bottom: 10rpx;
  left: 30rpx;
  padding: 2rpx 20rpx;
  background: rgba(255, 96, 96, .6);
  border-radius: 10rpx;
}

/* 猜你喜欢 */

.like {
  height: auto;
  padding: 12rpx 0;
}

.like .list .box {
  display: inline-block;
  box-sizing: border-box;
  width: 50%;
  padding: 10rpx;
  text-align: center;
}

.like .list view image {
  height: 360rpx;
  width: 300rpx; 
  border-radius: 16rpx;
  /* box-shadow: 0 0 4rpx #c97276; */
}

.like .list .tip text {
  font-size: 28rpx;
  color: #444;
}

.like .list .tip .price {
  font-size: 24rpx;
  color: red;
}

.type-navbar-item text {
  border-bottom: 4rpx solid #fff;
}

.type-item-on text {
  border-bottom: 4rpx solid #c97276;
}

</style>