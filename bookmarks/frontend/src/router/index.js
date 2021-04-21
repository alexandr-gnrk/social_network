import Vue from 'vue'
import VueRouter from 'vue-router'

import Dashboard from '../views/Dashboard.vue'
import Register from '../views/Register.vue'
import Login from '../views/Login.vue'
import Logout from '../views/Logout.vue'
import ChangePassword from '../views/ChangePassword'
import ImageList from '../views/ImageList'
import ImageDetail from '../views/ImageDetail'
import ImageRanking from '../views/ImageRanking'
import Notifications from '../views/Notifications'
import UserList from '../views/UserList'
import UserDetail from '../views/UserDetail'


Vue.use(VueRouter)

const PUBLIC_PATH_NAMES = ['login', 'register', 'logout',]

const routes = [
  {
    path: '/',
    name: 'dashboard',
    component: Dashboard
  },
  {
    path: '/register',
    name: 'register',
    component: Register
  },
  {
    path: '/login',
    name: 'login',
    component: Login
  },
  {
    path: '/logout',
    name: 'logout',
    component: Logout
  },
  {
    path: '/change-password',
    name: 'change-password',
    component: ChangePassword
  },
  {
    path: '/image-list',
    name: 'image-list',
    component: ImageList,
  },
  {
    path: '/image-list/:id',
    name: 'image-detail',
    component: ImageDetail,
    // props: true
  },
  {
    path: '/image-ranking',
    name: 'image-ranking',
    component: ImageRanking
  },
  {
    path: '/send',
    name: 'notifications',
    component: Notifications
  },
  {
    path: '/user-list',
    name: 'user-list',
    component: UserList
  },
  {
    path: '/user-list/:id',
    name: 'user-detail',
    component: UserDetail,
  },  
  {
    path: '*',
    redirect: {name: 'dashboard'}
  },  
]

const router = new VueRouter({
  mode: 'history',
  routes
})

router.beforeEach((to, from, next) => {
  if (!PUBLIC_PATH_NAMES.includes(to.name) && localStorage.getItem('token') == null && localStorage.getItem('token') == undefined){
    next('/login/?next=' + to.path);
  }else{
    next();
  }
});

export default router;
