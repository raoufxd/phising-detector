//import icons from material-ui
import {
    HomeOutlined,
} from '@ant-design/icons';


//import views
import HomePage from "./views/homePage";


const routes = [
    {
        path: "/home",
        name: "Home",
        icon: HomeOutlined,
        component: HomePage,
    },
];

export default routes;