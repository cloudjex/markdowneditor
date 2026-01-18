import {
  Alert, Button, Container, Dialog, DialogActions, DialogContent, DialogTitle, TextField
} from "@mui/material";
import { useState } from 'react';
import { useNavigate } from 'react-router-dom';

import loadingState from "../store/loading_store";
import userStore from '../store/user_store';
import request_utils from "../utils/request_utils";
import tree_utils from "../utils/tree_utils";

import type { TreeOperateResponse } from "../types/types";

function TreeUpdate(props: { currentNodeId: string }) {
  const navigate = useNavigate();

  const { id_token, node_tree, setNodeTree } = userStore();
  const root_node_id = node_tree.id;
  const { setLoading } = loadingState();

  const [postModalOpen, setPostModalOpen] = useState<boolean>(false);
  const [delModalOpen, setDelModalOpen] = useState<boolean>(false);
  const [isInvalidId, setIsInvalidId] = useState<boolean>(false);
  const [newNodeLabel, setNewNodeLabel] = useState<string>("");

  const onClickPostModal = () => {
    setNewNodeLabel("");
    setPostModalOpen(true);
  };

  const onClickDelModal = () => {
    setDelModalOpen(true);
  };

  const closeModal = () => {
    setNewNodeLabel("");
    setIsInvalidId(false);
    setPostModalOpen(false);
    setDelModalOpen(false);
  };

  const clickCreateNewContent = async () => {
    if (!newNodeLabel) {
      setIsInvalidId(true);
      throw new Error(`tree or newContentName is invalid`);
    };

    closeModal();
    setLoading(true);

    const res_promise = request_utils.requests<TreeOperateResponse>(
      `${import.meta.env.VITE_API_HOST}/api/trees/operate`,
      "PUT",
      { authorization: `Bearer ${id_token}` },
      { parent_id: `${props.currentNodeId}`, label: newNodeLabel }
    );
    const res = await res_promise;

    setNodeTree(res.body.node_tree);
    setLoading(false);
  };

  const clickDeleteContent = async () => {
    closeModal();
    setLoading(true);

    const delete_node_id = props.currentNodeId;
    const parent_node = tree_utils.get_parent_node(node_tree, delete_node_id);
    if (!parent_node) {
      throw new Error(`parent_node is null`);
    }
    const parent_id = parent_node.id;

    const res_promise = request_utils.requests<TreeOperateResponse>(
      `${import.meta.env.VITE_API_HOST}/api/trees/operate`,
      "DELETE",
      { authorization: `Bearer ${id_token}` },
      { id: delete_node_id }
    );
    const res = await res_promise;

    setLoading(false);
    setNodeTree(res.body.node_tree);
    navigate(`/main?id=${parent_id}`);
  };

  return (
    <>
      <Container sx={{
        my: 2,
        display: "flex",
        justifyContent: "center"
      }}>

        <Button
          onClick={onClickPostModal}
          size="small"
          disabled={props.currentNodeId === ""}
          variant="outlined"
          sx={{ mr: 1 }}
        >
          追加
        </Button>

        <Button
          onClick={onClickDelModal}
          size="small"
          disabled={props.currentNodeId === root_node_id}
          variant="outlined"
          color="error"
        >
          削除
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
            value={newNodeLabel}
            onChange={(e) => setNewNodeLabel(e.target.value)}
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