import {
  Alert, Button, Container, Dialog, DialogActions, DialogContent, DialogTitle, TextField
} from "@mui/material";
import { useState } from 'react';
import { useNavigate } from 'react-router-dom';

import RequestHandler from "@/lib/request_handler";
import TreeHandler from '@/lib/tree_handler';
import type { Tree } from "@/lib/types";
import loadingState from "@/store/loading_store";
import userStore from '@/store/user_store';


function TreeUpdate(props: { nodeId: string, tree: Tree }) {
  const navigate = useNavigate();
  const { idToken, setTree } = userStore();
  const { setLoading } = loadingState();

  const [labelInput, setLabelInput] = useState({
    label: "",
    isInvalid: false,
  });
  // 0: null, 1: post, 2: del
  const [dialogKind, setDialogKind] = useState(0);

  const requests = new RequestHandler(idToken);
  const treeHandler = new TreeHandler(props.tree);

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

    await requests.post(
      `/api/nodes/${props.nodeId}`,
      { label: label, text: "" }
    );

    const res = await requests.get<Tree>(
      `/api/tree`,
    );

    setTree(res.body);
    setLoading(false);
  };

  async function clickDeleteContent() {
    closeDialog();
    setLoading(true);

    const del_node_id = props.nodeId;
    const parent_node = treeHandler.getParentNode(del_node_id);
    const next_node_id = parent_node?.node_id || props.tree.node_id;

    await requests.delete(
      `/api/nodes/${del_node_id}`,
    );

    const res = await requests.get<Tree>(
      `/api/tree`,
    );

    setTree(res.body);
    setLoading(false);
    navigate(`/node/${next_node_id}`);
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
          disabled={props.nodeId === props.tree.node_id}
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
            value={treeHandler.getNode(props.nodeId)?.label}
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
          sx={{ fontSize: "80%" }}
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
