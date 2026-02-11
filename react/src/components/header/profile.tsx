import {
  Avatar, IconButton, Menu, MenuItem, Tooltip
} from "@mui/material";
import { useState } from 'react';

import type { Tree } from "@/src/lib/types";

import RequestHandler from "@/src/lib/request_handler";
import loadingState from "@/src/store/loading_store";
import userStore from '@/src/store/user_store';


function Profile() {
  const { email, id_token, setTree } = userStore();
  const { setLoading } = loadingState();
  const [isMenuOpen, setIsMenuOpen] = useState<null | HTMLElement>(null);

  const requests = new RequestHandler(id_token);

  async function clickReload() {
    setIsMenuOpen(null);
    setLoading(true);

    const res = await requests.get<Tree>(
      `/api/tree`,
    );

    setTree(res.body);
    setLoading(false);
    window.location.reload();
  };

  async function clickSignout() {
    setIsMenuOpen(null);
    setLoading(true);

    await requests.post(
      `/api/signout`,
    );

    setLoading(false);
    window.location.href = "/";
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
          <Avatar />
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

        <MenuItem onClick={clickReload} sx={{ fontSize: "80%" }}>
          リロード
        </MenuItem>
        <MenuItem onClick={clickSignout} sx={{ fontSize: "80%" }}>
          サインアウト
        </MenuItem>

      </Menu>
    </>
  );
}

export default Profile;
