import { Avatar } from "@mui/material";
import Button from '@mui/material/Button';
import Dialog from '@mui/material/Dialog';
import DialogActions from '@mui/material/DialogActions';
import DialogTitle from '@mui/material/DialogTitle';
import IconButton from '@mui/material/IconButton';
import Menu from '@mui/material/Menu';
import MenuItem from '@mui/material/MenuItem';
import Tooltip from '@mui/material/Tooltip';
import { useState } from 'react';
import { useNavigate } from "react-router-dom";

import userStore from '../store/user_store.jsx';
import utils from "../utils/utils.js";

import Loading from './loading.jsx';

function Profile() {
  const navigate = useNavigate();

  const { email, id_token } = userStore();
  const [isLoading, setLoading] = useState(false);
  const [isMenuOpen, setIsMenuOpen] = useState(null);
  const [isOpenLogoutDialog, setOpenLogoutDialog] = useState(false);

  const handleMenuOpen = (event) => {
    setIsMenuOpen(event.currentTarget);
  };

  const handleMenuClose = () => {
    setIsMenuOpen(null);
  };

  const clickInformation = (path) => {
    window.open(path);
    handleMenuClose();
  };

  const openLogout = () => {
    setOpenLogoutDialog(true);
    handleMenuClose();
  };

  const logOutClick = async () => {
    setOpenLogoutDialog(false);

    setLoading(true);
    await utils.requests(
      `${import.meta.env.VITE_API_HOST}/logout`,
      "POST",
      { authorization: `Bearer ${id_token}` },
      {}
    );
    setLoading(false);

    userStore.getState().reset();
    navigate("/");
  };

  if (id_token && email) {
    return (
      <>
        <Loading loading={isLoading} />

        <IconButton
          color="inherit"
          onClick={handleMenuOpen}
          sx={{ position: "absolute", right: 10 }}
        >
          <Tooltip title={`${email} でログイン中`}>
            <Avatar>{email.charAt(0).toUpperCase()}</Avatar>
          </Tooltip>
        </IconButton>

        <Menu
          anchorEl={isMenuOpen}
          open={Boolean(isMenuOpen)}
          onClose={handleMenuClose}
          anchorOrigin={{ vertical: "bottom", horizontal: "right" }}
          transformOrigin={{ vertical: "top", horizontal: "right" }}
          slotProps={{
            list: {
              'aria-labelledby': 'basic-button',
            },
          }}
        >
          <MenuItem onClick={() => clickInformation("/information")}>
            Information
          </MenuItem>
          <MenuItem onClick={() => clickInformation("https://github.com/katagiri1999/cork-up")}>
            Github
          </MenuItem>
          <MenuItem onClick={openLogout}>
            ログアウト
          </MenuItem>
        </Menu>

        <Dialog
          open={isOpenLogoutDialog}
          onClose={() => setOpenLogoutDialog(false)}
        >
          <DialogTitle>
            <b>{email}</b> からログアウトしますか？
          </DialogTitle>
          <DialogActions>
            <Button onClick={logOutClick}>はい</Button>
          </DialogActions>
        </Dialog>
      </>
    );
  };
}

export default Profile;