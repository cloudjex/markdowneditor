import MenuIcon from '@mui/icons-material/Menu';
import { Container, Drawer, IconButton, Tooltip, Typography } from '@mui/material';
import { useState } from 'react';

import type { Tree } from "@/src/lib/types";


import Explorer from '@/src/components/side_bar/explorer';
import TreeUpdate from '@/src/components/side_bar/tree_update';


function Sidebar(props: { tree: Tree, node_id: string }) {
  const [drawewrOpen, setDrawerOpen] = useState(false);

  return (
    <>
      <IconButton
        color="inherit"
        size='large'
        edge="start"
        onClick={() => {
          setDrawerOpen((prevState) => !prevState);
        }}
      >
        <Tooltip title="Menu">
          <MenuIcon
            sx={{ fontSize: 30 }}
          />
        </Tooltip>
      </IconButton>

      <Drawer
        open={drawewrOpen}
        onClose={(_, reason) => {
          if (reason === 'backdropClick') {
            setDrawerOpen(false);
          }
        }}
        sx={{
          '& .MuiDrawer-paper': { boxSizing: 'border-box', width: 300 },
        }}
      >

        <Container sx={{ textAlign: 'left' }}>

          <Typography variant="h5" sx={{ mt: 2 }}>
            Explorer
          </Typography>

          <TreeUpdate node_id={props.node_id} tree={props.tree} />
          <Explorer node_id={props.node_id} tree={props.tree} />

        </Container>
      </Drawer >
    </>
  );
}

export default Sidebar;
