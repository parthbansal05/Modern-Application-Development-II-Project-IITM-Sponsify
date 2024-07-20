import Vue from "vue";
import Router from "vue-router";

// Import your components here
import HomePage from "@/components/HomePage.vue";
import AboutPage from "@/components/AboutPage.vue";
import GetData from "@/components/GetData.vue";

Vue.use(Router);

export default new Router({
  mode: "history", // Use HTML5 History mode
  routes: [
    {
      path: "/",
      name: "HomePage",
      component: HomePage,
    },
    {
      path: "/about",
      name: "AboutPage",
      component: AboutPage,
    },
    {
      path: "/getdata",
      name: "GetData",
      component: GetData,
    },
  ],
});
