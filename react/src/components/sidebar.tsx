import MenuIcon from '@mui/icons-material/Menu';
import { Container, Drawer, IconButton, Tooltip } from '@mui/material';
import { useState } from 'react';

import Explorer from './explorer';

function Sidebar() {
  const [drawewrOpen, setDrawerOpen] = useState<boolean>(false);

  const handleDrawerToggle = () => {
    setDrawerOpen((prevState) => !prevState);
  };

  return (
    <>
      <IconButton
        color="inherit"
        aria-label="open drawer"
        edge="start"
        onClick={handleDrawerToggle}
        size='large'
        sx={{ mr: 2 }}
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

          <Explorer />

        </Container>
      </Drawer >
    </>
  );
}

export default Sidebar;