<template>
<!--miniprogram/pages/menu/menu.wxml-->
<view class="menu">
  <view v-for="(item, index) in list" :key="index" class="item">
    <view class="title">
      <image src="/static/images/tags.png"></image>
      <text>{{item.name}}</text>
    </view>
    <view class="classic">
      <text v-for="(item, index2) in item.list" :key="index2" :data-tags="item.id" :data-content="item.name" @tap="goList">{{item.name}}</text> 
    </view> 
  </view> 
</view>
</template>

<script>

export default {
  data() {
    return {
      list: [],
      loading: false
    };
  },

  components: {},
  props: {},

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    this.loadList();
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
  onShareAppMessage: function () {},
  methods: {
    // 获取列表数据
    loadList() {
      let {
        list
      } = this;
      uni.showLoading({
        title: '正在加载...',
        mask: true
      });
      this.$scope.setData({
        loading: true
      }); // 从云数据库读取列表

      const db = uniCloud.database();
      db.collection('foods').doc('categorys').get().then(res => {
        console.log(res.data.category_list);
        list.push(...res.data.category_list);
        this.$scope.setData({
          list
        });
        console.log(list);
        uni.hideLoading();
      });
    },

    goList(e) {
      console.log(e);
      uni.navigateTo({
        url: `/pages/list/list?content=${e.currentTarget.dataset.content}&tags=${e.currentTarget.dataset.tags}`
      });
    }

  }
};
</script>
<style>
/* miniprogram/pages/menu/menu.wxss */
.menu {
  padding: 20rpx;
  font-size: 28rpx;
}
.menu image {
  height: 40rpx;
  width: 40rpx;
  margin-right: 10rpx;
}
.menu .item {
  margin-bottom: 30rpx;
}
.menu .title {
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 34rpx;
  color: #555;
}
.menu .item .classic {
  display: flex;
  flex-wrap: wrap;
  padding: 20rpx 0;
  justify-content: center;
  align-items: center;
}
.menu .item .classic text {
  border: 1px solid #f8dada;
  padding: 10rpx 20rpx;
  margin: 20rpx;
  color: #777;
  font-size: 24rpx;
  border-radius: 18rpx;
}

</style>