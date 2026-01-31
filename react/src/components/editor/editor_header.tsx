import MoreVertIcon from '@mui/icons-material/MoreVert';
import { Alert, Box, Button, Dialog, DialogActions, DialogContent, DialogTitle, IconButton, Menu, MenuItem, Select, TextField } from '@mui/material';
import fileDownload from 'js-file-download';
import { useState } from 'react';

import type { Tree } from '@/src/lib/types';

import RequestHandler from "@/src/lib/request_handler";
import TreeHandler from '@/src/lib/tree_handler';
import loadingState from "@/src/store/loading_store";
import userStore from '@/src/store/user_store';


function EditorHeader(props: { node_id: string, tree: Tree, text: string }) {
  const { id_token, setTree, setPreviewText } = userStore();
  const { setLoading } = loadingState();

  const [isMenuOpen, setIsMenuOpen] = useState<null | HTMLElement>(null);
  // 0: null, 1: label update, 2: move page
  const [modalKind, setModalKind] = useState(0);
  const [newLabel, setNewLabel] = useState("");
  const [isInvalid, setIsInvalid] = useState(false);
  const [destination, setDestination] = useState("");

  const requests = new RequestHandler(id_token);
  const tree_handler = new TreeHandler(props.tree);
  const node_list = tree_handler.getNodeList();
  const label = tree_handler.getNode(props.node_id)?.label;

  async function upload() {
    setLoading(true);

    await requests.put(
      `${import.meta.env.VITE_API_HOST}/api/nodes/${props.node_id}`,
      { text: props.text }
    );

    setLoading(false);
  };

  function closeModal() {
    setNewLabel("");
    setIsInvalid(false);
    setModalKind(0);
    setIsMenuOpen(null);
  };

  async function updateNodeLabel(node_id: string, label: string) {
    if (!label) {
      setIsInvalid(true);
      throw new Error("label is invalid");
    }

    closeModal();
    setLoading(true);

    const res = await requests.put<Tree>(
      `${import.meta.env.VITE_API_HOST}/api/tree/node/label/${node_id}`,
      { label: label }
    );

    setTree(res.body);
    setLoading(false);
  }

  async function updateMoveNode(node_id: string, parent_id: string = "") {
    if (!parent_id) {
      setIsInvalid(true);
      throw new Error("destination is invalid");
    }

    closeModal();
    setLoading(true);

    const res = await requests.put<Tree>(
      `${import.meta.env.VITE_API_HOST}/api/tree/node/move/${node_id}`,
      { parent_id: parent_id }
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
            closeModal();
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
              closeModal();
            }}
          >
            エクスポート
          </MenuItem>
          <MenuItem
            sx={{ fontSize: "80%" }}
            onClick={() => {
              setModalKind(1);
            }}
          >
            ラベル更新
          </MenuItem>
          <MenuItem
            sx={{ fontSize: "80%" }}
            onClick={() => {
              setModalKind(2);
            }}
            disabled={props.node_id === props.tree.id}
          >
            ページ移動
          </MenuItem>

        </Menu>

      </Box>

      <Dialog
        onClose={() => closeModal()}
        open={modalKind == 1}
      >
        <DialogTitle>
          ラベル更新
        </DialogTitle>

        <DialogContent>
          <TextField
            label="ラベルを入力してください"
            variant="standard"
            value={newLabel}
            onChange={(e) => setNewLabel(e.target.value)}
            sx={{ width: 300 }}
          />
        </DialogContent>

        {isInvalid &&
          <Alert severity="error" sx={{ mx: 3 }}>
            ラベルを入力してください。
          </Alert>
        }

        <DialogActions>
          <Button
            autoFocus
            onClick={() => updateNodeLabel(props.node_id, newLabel)}
          >
            OK
          </Button>
        </DialogActions>
      </Dialog>

      <Dialog
        onClose={() => closeModal()}
        open={modalKind == 2}
      >
        <DialogTitle>
          ページ移動
        </DialogTitle>

        <DialogContent>
          <Select
            value={destination}
            onChange={(e) => setDestination(e.target.value)}
            sx={{ width: 300 }}
          >
            {node_list.map((node) => (
              <MenuItem key={node.id} value={node.id}>
                {node.label}
              </MenuItem>
            ))}
          </Select>
        </DialogContent>

        {isInvalid &&
          <Alert severity="error" sx={{ mx: 3 }}>
            移動先を選択してください。
          </Alert>
        }

        <DialogActions>
          <Button
            autoFocus
            onClick={() => updateMoveNode(props.node_id, destination)}
          >
            OK
          </Button>
        </DialogActions>
      </Dialog>
    </>
  );
}

export default EditorHeader;