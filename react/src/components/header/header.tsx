import { AppBar, Toolbar, Typography } from '@mui/material';

import type { Tree } from "@/src/lib/types";

import Profile from '@/src/components/header/profile';
import Sidebar from '@/src/components/side_bar/sidebar';


function Header(props: { tree?: Tree, nodeId?: string }) {
  return (
    <AppBar position="static">
      <Toolbar style={{ display: "flex" }}>

        {props.tree && props.nodeId &&
          <Sidebar tree={props.tree} nodeId={props.nodeId} />
        }

        <Typography
          variant="h6"
        >
          cloudjex.com
        </Typography>

        {props.tree && props.nodeId &&
          <Profile />
        }

      </Toolbar>
    </AppBar>
  );

}

export default Header;
