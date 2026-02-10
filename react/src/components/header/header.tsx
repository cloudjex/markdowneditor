import { AppBar, Toolbar, Typography } from '@mui/material';

import type { Tree } from "@/src/lib/types";

import Profile from '@/src/components/header/profile';
import Sidebar from '@/src/components/side_bar/sidebar';


function Header(props: { tree?: Tree, node_id?: string }) {
  return (
    <AppBar position="static">
      <Toolbar style={{ display: "flex" }}>

        {props.tree && props.node_id &&
          <Sidebar tree={props.tree} node_id={props.node_id} />
        }

        <Typography
          variant="h6"
        >
          cloudjex.com
        </Typography>

        {props.tree && props.node_id &&
          <Profile />
        }

      </Toolbar>
    </AppBar>
  );

}

export default Header;
