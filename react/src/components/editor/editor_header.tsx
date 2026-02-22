import MoreVertIcon from '@mui/icons-material/MoreVert';
import { Alert, Box, Button, Dialog, DialogActions, DialogContent, DialogTitle, IconButton, Menu, MenuItem, Select, TextField } from '@mui/material';
import fileDownload from 'js-file-download';
import { useState } from 'react';

import type { Tree } from '@/src/lib/types';

import RequestHandler from "@/src/lib/request_handler";
import TreeHandler from '@/src/lib/tree_handler';
import loadingState from "@/src/store/loading_store";
import userStore from '@/src/store/user_store';


function EditorHeader(props: { tree: Tree, nodeId: string, text: string }) {
  const { idToken, setTree, setPreviewText } = userStore();
  const { setLoading } = loadingState();

  const [isMenuOpen, setIsMenuOpen] = useState<null | HTMLElement>(null);
  // 0: null, 1: label update, 2: move page
  const [dialogKind, setDialogKind] = useState(0);

  const [labelInput, setLabelInput] = useState({
    label: "",
    isInvalid: false,
  });
  const [moveInput, setMoveInput] = useState({
    parentId: "",
    isInvalid: false,
  });

  const requests = new RequestHandler(idToken);
  const treeHandler = new TreeHandler(props.tree);
  const nodeList = treeHandler.moveNodeList(props.nodeId);
  const label = treeHandler.getNode(props.nodeId)?.label;

  async function upload() {
    setLoading(true);

    await requests.put(
      `/api/nodes/${props.nodeId}`,
      { text: props.text, label: label }
    );

    setLoading(false);
  };

  function closeDialog() {
    setLabelInput({ label: "", isInvalid: false, });
    setMoveInput({ parentId: "", isInvalid: false, });
    setDialogKind(0);
    setIsMenuOpen(null);
  };

  async function updateNodeLabel() {
    if (!labelInput.label) {
      setLabelInput({ ...labelInput, isInvalid: true, });
      throw new Error("label is invalid");
    }

    closeDialog();
    setLoading(true);

    await requests.put(
      `/api/nodes/${props.nodeId}`,
      { text: props.text, label: labelInput.label }
    );

    const res = await requests.get<Tree>(
      `/api/tree`,
    );

    setTree(res.body);
    setLoading(false);
  }

  async function updateMoveNode() {
    if (!moveInput.parentId) {
      setMoveInput({ ...moveInput, isInvalid: true });
      throw new Error("destination is invalid");
    }

    closeDialog();
    setLoading(true);

    await requests.put<Tree>(
      `/api/nodes/move/${props.nodeId}`,
      { parent_id: moveInput.parentId }
    );

    const res = await requests.get<Tree>(
      `/api/tree`,
    );

    setTree(res.body);
    setLoading(false);
  }

  return (
    <>
      <Box
        sx={{ mb: 1 }}
      >
        <Button
          variant='outlined'
          size='small'
          onClick={() => {
            setPreviewText(props.text);
            window.open("/preview/state", '_blank');
          }}
        >
          プレビュー
        </Button>

        <Button
          variant='outlined'
          size='small'
          sx={{ ml: 1 }}
          onClick={upload}
        >
          保存
        </Button>

        <IconButton
          color="info"
          sx={{ ml: 1 }}
          onClick={(event: React.MouseEvent<HTMLElement>) => {
            setIsMenuOpen(event.currentTarget);
          }}
        >
          <MoreVertIcon />
        </IconButton>

        <Menu
          anchorEl={isMenuOpen}
          open={Boolean(isMenuOpen)}
          onClose={() => {
            closeDialog();
          }}
          anchorOrigin={{ vertical: "bottom", horizontal: "right" }}
          transformOrigin={{ vertical: "top", horizontal: "right" }}
          slotProps={{
            list: {
              'aria-labelledby': 'basic-button',
            },
          }}
        >

          <MenuItem
            sx={{ fontSize: "80%" }}
            onClick={() => {
              fileDownload(props.text, `${label}.md`);
              closeDialog();
            }}
          >
            エクスポート
          </MenuItem>
          <MenuItem
            sx={{ fontSize: "80%" }}
            onClick={() => {
              setDialogKind(1);
            }}
          >
            ラベル更新
          </MenuItem>
          <MenuItem
            sx={{ fontSize: "80%" }}
            onClick={() => {
              setDialogKind(2);
            }}
            disabled={props.nodeId === props.tree.node_id}
          >
            ページ移動
          </MenuItem>

        </Menu>

      </Box>

      <Dialog
        onClose={() => closeDialog()}
        open={dialogKind == 1}
      >
        <DialogTitle>
          ラベル更新
        </DialogTitle>

        <DialogContent>
          <TextField
            label="ラベルを入力してください"
            variant="standard"
            value={labelInput.label}
            onChange={(e) => setLabelInput({ ...labelInput, label: e.target.value })}
            sx={{ width: 300 }}
          />
        </DialogContent>

        {labelInput.isInvalid &&
          <Alert severity="error" sx={{ mx: 3 }}>
            ラベルを入力してください。
          </Alert>
        }

        <DialogActions>
          <Button
            autoFocus
            onClick={() => updateNodeLabel()}
          >
            OK
          </Button>
        </DialogActions>
      </Dialog>

      <Dialog
        onClose={() => closeDialog()}
        open={dialogKind == 2}
      >
        <DialogTitle>
          ページ移動
        </DialogTitle>

        <DialogContent>
          <Box sx={{ mb: 1, fontSize: "80%" }}>
            現在のページと配下のページを移動します。移動先を選択してください。
          </Box>

          <Select
            value={moveInput.parentId}
            onChange={(e) => setMoveInput({ ...moveInput, parentId: e.target.value })}
            sx={{ width: 300 }}
          >
            {nodeList.map((node) => (
              <MenuItem key={node.node_id} value={node.node_id}>
                {node.label}
              </MenuItem>
            ))}
          </Select>
        </DialogContent>

        {moveInput.isInvalid &&
          <Alert severity="error" sx={{ mx: 3 }}>
            移動先を選択してください。
          </Alert>
        }

        <DialogActions>
          <Button
            autoFocus
            onClick={() => updateMoveNode()}
          >
            OK
          </Button>
        </DialogActions>
      </Dialog>
    </>
  );
}

export default EditorHeader;
