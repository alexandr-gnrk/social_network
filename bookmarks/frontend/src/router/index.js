import Vue from 'vue'
import VueRouter from 'vue-router'
import Dashboard from '../views/Dashboard.vue'
import Register from '../views/Register.vue'
import Login from '../views/Login.vue'
import Logout from '../views/Logout.vue'


Vue.use(VueRouter)

const PUBLIC_PATH_NAMES = ['login', 'register', 'logout']

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
  }
]

const router = new VueRouter({
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