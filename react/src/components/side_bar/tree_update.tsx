import {
  Alert, Button, Container, Dialog, DialogActions, DialogContent, DialogTitle, TextField
} from "@mui/material";
import { useState } from 'react';
import { useNavigate } from 'react-router-dom';

import RequestHandler from "../../lib/request_handler";
import TreeHandler from '../../lib/tree_handler';
import loadingState from "../../store/loading_store";
import userStore from '../../store/user_store';

import type { NodeTree, TreeOperateResponse } from "../../lib/types";

function TreeUpdate(props: { node_id: string, node_tree: NodeTree }) {
  const navigate = useNavigate();
  const { id_token, setNodeTree } = userStore();
  const { setLoading } = loadingState();
  const root_node_id = props.node_tree.id;

  // 0: null, 1: post, 2: del
  const [modalKind, setModalKind] = useState(0);
  const [isInvalidLabel, setIsInvalidLabel] = useState(false);
  const [newNodeLabel, setNewNodeLabel] = useState("");

  const requests = new RequestHandler(id_token);
  const tree_handler = new TreeHandler(props.node_tree);
  const current_label = tree_handler.getNode(props.node_id)?.label;

  function closeModal() {
    setNewNodeLabel("");
    setIsInvalidLabel(false);
    setModalKind(0);
  };

  async function clickCreateNewContent() {
    if (!newNodeLabel) {
      setIsInvalidLabel(true);
      throw new Error("newContentName is invalid");
    };

    closeModal();
    setLoading(true);

    const res_promise = requests.post<TreeOperateResponse>(
      `${import.meta.env.VITE_API_HOST}/api/trees/operate`,
      { parent_id: props.node_id, label: newNodeLabel }
    );
    const res = await res_promise;

    setNodeTree(res.body.node_tree);
    setLoading(false);
  };

  async function clickDeleteContent() {
    closeModal();
    setLoading(true);

    const delete_node_id = props.node_id;
    const parent_node = tree_handler.getParentNode(delete_node_id);
    const next_node = parent_node?.id || props.node_tree.id;

    const res_promise = requests.delete<TreeOperateResponse>(
      `${import.meta.env.VITE_API_HOST}/api/trees/operate`,
      { id: delete_node_id }
    );
    const res = await res_promise;

    setLoading(false);
    setNodeTree(res.body.node_tree);
    navigate(`/main?id=${next_node}`);
  };

  return (
    <>
      <Container sx={{
        my: 2,
        display: "flex",
        justifyContent: "center"
      }}>

        <Button
          onClick={() => setModalKind(1)}
          size="small"
          variant="outlined"
          sx={{ mr: 1 }}
        >
          追加
        </Button>

        <Button
          onClick={() => setModalKind(2)}
          size="small"
          disabled={props.node_id === root_node_id}
          variant="outlined"
          color="error"
        >
          削除
        </Button>

      </Container>

      <Dialog onClose={closeModal} open={modalKind == 1}>
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
            value={`${current_label}/`}
          />
          <TextField
            id="outlined-basic"
            label="Node"
            variant="outlined"
            value={newNodeLabel}
            onChange={(e) => setNewNodeLabel(e.target.value)}
          />
        </Container>

        {isInvalidLabel &&
          <Alert severity="error" sx={{ mx: 3 }}>
            Node名を入力してください。
          </Alert>
        }

        <DialogActions>
          <Button autoFocus onClick={clickCreateNewContent}>OK</Button>
        </DialogActions>

      </Dialog>

      <Dialog onClose={closeModal} open={modalKind == 2}>
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