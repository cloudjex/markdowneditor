import DeleteOutlineOutlinedIcon from '@mui/icons-material/DeleteOutlineOutlined';
import NoteAddOutlinedIcon from '@mui/icons-material/NoteAddOutlined';
import Alert from "@mui/material/Alert";
import Button from "@mui/material/Button";
import Container from "@mui/material/Container";
import Dialog from '@mui/material/Dialog';
import DialogActions from '@mui/material/DialogActions';
import DialogContent from "@mui/material/DialogContent";
import DialogTitle from '@mui/material/DialogTitle';
import TextField from '@mui/material/TextField';
import { useState } from 'react';
import { useNavigate } from 'react-router-dom';

import loadingState from "../store/loading_store";
import userStore from '../store/user_store';
import utils from "../utils/utils";

import type { TreeNode } from "../types/types";

function TreeUpdate(props: { currentNodeId: string }) {
  const navigate = useNavigate();

  const { id_token, tree, setTree } = userStore();
  const { setLoading } = loadingState();

  const [postModalOpen, setPostModalOpen] = useState(false);
  const [delModalOpen, setDelModalOpen] = useState(false);
  const [isInvalidId, setIsInvalidId] = useState(false);
  const [newContentName, setNewContentName] = useState("");

  const onClickPostModal = () => {
    setNewContentName("");
    setPostModalOpen(true);
  };

  const onClickDelModal = () => {
    setDelModalOpen(true);
  };

  const closeModal = () => {
    setNewContentName("");
    setIsInvalidId(false);
    setPostModalOpen(false);
    setDelModalOpen(false);
  };

  const clickCreateNewContent = async () => {
    if (!tree) {
      throw new Error(`tree is null`);
    };

    const new_node_id = `${props.currentNodeId}/${newContentName}`;
    const isValid = utils.is_valid_new_node(tree, new_node_id);
    if (!isValid) {
      setIsInvalidId(true);
      return;
    }

    closeModal();
    setLoading(true);

    const res_promise = utils.requests(
      `${import.meta.env.VITE_API_HOST}/trees/operate`,
      "PUT",
      { authorization: `Bearer ${id_token}` },
      { node_id: new_node_id }
    );
    const res = await res_promise;
    const body = res.body as { tree: TreeNode };

    setTree(body.tree);
    setLoading(false);
  };

  const clickDeleteContent = async () => {
    closeModal();
    setLoading(true);

    const delete_node_id = props.currentNodeId;
    const next_current_id = utils.get_parent_node_id(delete_node_id);

    const res_promise = utils.requests(
      `${import.meta.env.VITE_API_HOST}/trees/operate`,
      "DELETE",
      { authorization: `Bearer ${id_token}` },
      { node_id: delete_node_id }
    );
    const res = await res_promise;
    const body = res.body as { tree: TreeNode };

    setTree(body.tree);
    navigate(`/main?node_id=${next_current_id}`);
  };

  return (
    <>
      <Container sx={{
        m: 3,
        display: "flex"
      }}>

        <Button onClick={onClickPostModal} disabled={props.currentNodeId === ""}>
          <NoteAddOutlinedIcon />
        </Button>

        <Button onClick={onClickDelModal} disabled={props.currentNodeId === "" || props.currentNodeId === '/Nodes'} sx={{ color: "red" }}>
          <DeleteOutlineOutlinedIcon />
        </Button>

      </Container>

      <Dialog onClose={closeModal} open={postModalOpen}>
        <DialogTitle>
          Nodeを作成
        </DialogTitle>

        <Container
          component="form"
          sx={{ '& > :not(style)': { m: 2, width: '25ch' } }}
          noValidate
          autoComplete="off"
        >
          <TextField
            id="outlined-basic"
            label="親Node"
            variant="outlined"
            disabled
            value={`${props.currentNodeId}/`}
          />
          <TextField
            id="outlined-basic"
            label="Node"
            variant="outlined"
            value={newContentName}
            onChange={(e) => setNewContentName(e.target.value)}
          />
        </Container>

        {isInvalidId &&
          <Alert severity="error" sx={{ mx: 3 }}>
            Node名を確認してください。すでに存在するNode名、または不正な文字列が含まれています。
          </Alert>
        }

        <DialogActions>
          <Button autoFocus onClick={clickCreateNewContent}>OK</Button>
        </DialogActions>

      </Dialog>

      <Dialog onClose={closeModal} open={delModalOpen}>
        <DialogTitle>
          Nodeを削除
        </DialogTitle>

        <DialogContent>
          現在のNodeとすべての子Nodeが削除されます。
          削除しますか？
        </DialogContent>

        <DialogActions>
          <Button autoFocus onClick={clickDeleteContent} sx={{ color: "red" }}>OK</Button>
        </DialogActions>

      </Dialog>
    </>
  );
};

export default TreeUpdate;