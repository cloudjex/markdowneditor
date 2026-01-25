import {
  Avatar, IconButton, Menu, MenuItem, Tooltip
} from "@mui/material";
import { useState } from 'react';
import { useNavigate } from "react-router-dom";

import RequestHandler from "@/src/lib/request_handler";
import loadingState from "@/src/store/loading_store";
import userStore from '@/src/store/user_store';


function Profile() {
  const navigate = useNavigate();
  const { email, id_token } = userStore();
  const { setLoading } = loadingState();
  const [isMenuOpen, setIsMenuOpen] = useState<null | HTMLElement>(null);

  const requests = new RequestHandler(id_token);

  async function clickSignout() {
    setIsMenuOpen(null);
    setLoading(true);

    const res_promise = requests.post(
      `${import.meta.env.VITE_API_HOST}/api/signout`,
    );
    await res_promise;

    setLoading(false);
    navigate("/");
  };

  return (
    <>
      <IconButton
        color="inherit"
        onClick={(event: React.MouseEvent<HTMLElement>) => {
          setIsMenuOpen(event.currentTarget);
        }}
        sx={{ position: "absolute", right: 10 }}
      >

        <Tooltip title={`Sign In: ${email}`}>
          <Avatar>{email.charAt(0).toUpperCase()}</Avatar>
        </Tooltip>

      </IconButton>

      <Menu
        anchorEl={isMenuOpen}
        open={Boolean(isMenuOpen)}
        onClose={() => {
          setIsMenuOpen(null);
        }}
        anchorOrigin={{ vertical: "bottom", horizontal: "right" }}
        transformOrigin={{ vertical: "top", horizontal: "right" }}
        slotProps={{
          list: {
            'aria-labelledby': 'basic-button',
          },
        }}
      >

        <MenuItem onClick={clickSignout} sx={{ fontSize: "80%" }}>
          サインアウト
        </MenuItem>

      </Menu>
    </>
  );
}

export default Profile;