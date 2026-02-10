import {
  Alert, Button, Container, Dialog, DialogActions, DialogContent, DialogTitle, TextField
} from "@mui/material";
import { useState } from 'react';
import { useNavigate } from 'react-router-dom';

import type { Tree } from "@/src/lib/types";

import RequestHandler from "@/src/lib/request_handler";
import TreeHandler from '@/src/lib/tree_handler';
import loadingState from "@/src/store/loading_store";
import userStore from '@/src/store/user_store';


function TreeUpdate(props: { node_id: string, tree: Tree }) {
  const navigate = useNavigate();
  const { id_token, setTree } = userStore();
  const { setLoading } = loadingState();

  const [labelInput, setLabelInput] = useState({
    label: "",
    isInvalid: false,
  });
  // 0: null, 1: post, 2: del
  const [dialogKind, setDialogKind] = useState(0);

  const requests = new RequestHandler(id_token);
  const tree_handler = new TreeHandler(props.tree);

  function closeDialog() {
    setLabelInput({ label: "", isInvalid: false, });
    setDialogKind(0);
  };

  async function clickCreateNewContent(label: string) {
    if (!label) {
      setLabelInput({ ...labelInput, isInvalid: true });
      throw new Error("newContentName is invalid");
    };

    closeDialog();
    setLoading(true);

    const res = await requests.post<Tree>(
      `${import.meta.env.VITE_API_HOST}/api/tree/node`,
      { parent_id: props.node_id, label: label }
    );

    setTree(res.body);
    setLoading(false);
  };

  async function clickDeleteContent() {
    closeDialog();
    setLoading(true);

    const del_node_id = props.node_id;
    const parent_node = tree_handler.getParentNode(del_node_id);
    const next_node_id = parent_node?.node_id || props.tree.node_id;

    const res = await requests.delete<Tree>(
      `${import.meta.env.VITE_API_HOST}/api/tree/node/${del_node_id}`,
    );

    setLoading(false);
    setTree(res.body);
    navigate(`/main/${next_node_id}`);
  };

  return (
    <>
      <Container sx={{
        my: 2,
        display: "flex",
        justifyContent: "center"
      }}>

        <Button
          onClick={() => setDialogKind(1)}
          size="small"
          variant="outlined"
          sx={{ mr: 1 }}
        >
          追加
        </Button>

        <Button
          onClick={() => setDialogKind(2)}
          size="small"
          disabled={props.node_id === props.tree.node_id}
          variant="outlined"
          color="error"
        >
          削除
        </Button>

      </Container>

      <Dialog onClose={closeDialog} open={dialogKind == 1}>
        <DialogTitle>
          ページを作成
        </DialogTitle>

        <Container
          component="form"
          sx={{ '& > :not(style)': { m: 2, width: '25ch' } }}
          noValidate
        >
          <TextField
            id="outlined-basic"
            label="親ラベル"
            variant="standard"
            disabled
            value={tree_handler.getNode(props.node_id)?.label}
          />
          <TextField
            id="outlined-basic"
            label="ラベルを入力してください"
            variant="standard"
            value={labelInput.label}
            onChange={(e) => setLabelInput({ ...labelInput, label: e.target.value })}
          />
        </Container>

        {labelInput.isInvalid &&
          <Alert severity="error" sx={{ mx: 3 }}>
            ラベルを入力してください。
          </Alert>
        }

        <DialogActions>
          <Button
            autoFocus
            onClick={() => clickCreateNewContent(labelInput.label)}
          >
            OK
          </Button>
        </DialogActions>

      </Dialog>

      <Dialog onClose={closeDialog} open={dialogKind == 2}>
        <DialogTitle>
          ページを削除
        </DialogTitle>

        <DialogContent
          sx={{fontSize: "80%"}}
        >
          現在のページとその配下のページを削除します。よろしいですか？
        </DialogContent>

        <DialogActions>
          <Button autoFocus onClick={clickDeleteContent} sx={{ color: "red" }}>OK</Button>
        </DialogActions>

      </Dialog>
    </>
  );
};

export default TreeUpdate;
