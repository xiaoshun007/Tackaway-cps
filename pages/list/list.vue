<template>
<!--miniprogram/pages/list/list.wxml-->
<scroll-view scroll-y="true" style="height:100%;" lower-threshold="50" @scrolltolower="lower">
  <!-- <view class='box' wx:for='{{list}}' wx:key='{{index}}'>
    <text>{{item.title}}</text>
  </view>  -->
  <view v-for="(item, index) in list" :key="index" class="box" :data-id="item.id" @tap="goDetail">
    <image :src="item.albums[0]"></image>
    <view class="right">
      <text class="title">{{item.title}}</text>
      <text>原料：{{item.ingredients}}</text>
      <text>用料：{{item.burden}}</text>
      <text class="see">{{item.count}} 人浏览</text>
    </view>
  </view>
  
  <view class="loading" v-if="loading" style="text-align:center;">
    <image src="/static/images/loading/loading-bars.svg" style="height: 60px;"></image>
  </view>
  <view class="bottom" v-if="isOver" style="text-align:center;font-size:24rpx;padding:30rpx;">
    <text style="color:#666;">--- 我是有底线的 ---</text>
  </view>
  <view class="no-list" v-if="noList" style="text-align:center;font-size:24rpx;padding:30rpx;">
    <text style="color:#666;">--- 未找到您搜索的菜品 ---</text>
  </view>
</scroll-view>
</template>

<script>

export default {
  data() {
    return {
      list: [],
      index: 0,
      // 页码起始下标
      num: 10,
      // 每页展示个数
      searchContent: '',
      // 搜索内容或者搜索标签id
      searchIsTags: false,
      // 是否搜索的是标签id
      loading: false,
      // 是否正在加载
      isOver: false,
      // 滑动到底
      noList: false // 搜索结果为空

    };
  },

  components: {},
  props: {},

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    uni.setNavigationBarTitle({
      title: options.content //页面标题为路由参数

    });
    console.log(options);

    if (options.tags) {
      this.searchContent = options.content;
      this.searchIsTags = true;
      this.loadList(options.content);
    } else {
      this.searchContent = options.content;
      this.loadList(options.content);
    }
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
	// 加载列表
	loadList(content) {
	  let that = this;
	  const db = uniCloud.database();
	
	  if (!this.isOver) {
	    let {
	      list,
	      index,
	      num
	    } = this;
	    uni.showLoading({
	      title: '正在加载...',
	      mask: true
	    });
		loading: true
	    this.$scope.setData({
	      loading: true
	    }); // 从云数据库读取列表
	
	    const db = uniCloud.database();
	    const MAX_LIMIT = 8;
	    db.collection('foods').skip(index).limit(MAX_LIMIT).where({
	      category: content
	    }).get().then(res => {
	      console.log(res);
	
	      if (res.result.data.length) {
	        list.push(...res.result.data);
	        this.$scope.setData({
	          list,
	          index: index + MAX_LIMIT,
	          loading: false
	        });
	        console.log(list);
	      } else {
	        this.$scope.setData({
	          loading: false,
	          isOver: true
	        });
	      }
	
	      uni.hideLoading();
	    });
	  }
	},
	
    goDetail(e) {
      console.log('detail');
      console.log(e.currentTarget.dataset.id);
      uni.navigateTo({
        url: `/pages/detail/detail?id=${e.currentTarget.dataset.id}`
      });
    },

    // 上拉加载
    lower() {
      console.log('lower');

      if (!this.loading) {
        if (this.searchIsTags) {
          this.loadList(this.searchContent);
        } else {
          this.loadList(this.searchContent);
        }
      }
    }

  }
};
</script>
<style>
/* miniprogram/pages/list/list.wxss */

.box {
  border: 1px solid #ddd;
  margin: 20rpx 30rpx 40rpx 30rpx;
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
  color: #FF6262;
  padding-top: 10rpx;
}
</style>