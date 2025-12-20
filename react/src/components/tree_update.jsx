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
import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';

import userStore from '../store/user_store';
import utils from "../utils/utils";

import Loading from './loading';

function TreeUpdate(props) {
  const navigate = useNavigate();

  const { id_token, tree, setTree } = userStore();
  const [isLoading, setLoading] = useState(false);

  const [postModalOpen, setPostModalOpen] = useState(false);
  const [delModalOpen, setDelModalOpen] = useState(false);
  const [isInvalidId, setIsInvalidId] = useState(false);
  const [currentNodeId, setCurrentNodeId] = useState("");
  const [newContentName, setNewContentName] = useState("");

  useEffect(() => {
    setCurrentNodeId(props.currentNodeId);
  }, [props.currentNodeId]);

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
    const insert_node = { id: `${currentNodeId}/${newContentName}`, label: newContentName };

    var isValid = utils.is_valid_new_node(tree, insert_node);
    if (!isValid) {
      setIsInvalidId(true);
      return;
    }

    const new_tree = utils.insert_node(tree, insert_node);

    setLoading(true);
    closeModal();

    var res = utils.requests(
      `${import.meta.env.VITE_API_HOST}/trees`,
      "PUT",
      { authorization: `Bearer ${id_token}` },
      { tree: new_tree }
    );
    res = await res;

    setTree(res.body.tree);
    setLoading(false);
  };

  const clickDeleteContent = async () => {
    setLoading(true);
    closeModal();

    var parents = utils.get_parent_node_ids(currentNodeId);
    const next_current_id = parents[parents.length - 1];
    var new_tree = utils.delete_tree_node(tree, currentNodeId);

    var res = utils.requests(
      `${import.meta.env.VITE_API_HOST}/trees`,
      "PUT",
      { authorization: `Bearer ${id_token}` },
      { tree: new_tree }
    );
    res = await res;

    setTree(res.body.tree);
    setLoading(false);
    navigate(`/main?node_id=${next_current_id}`);
  };

  return (
    <>
      <Loading loading={isLoading} />

      <Container sx={{
        m: 3,
        display: "flex"
      }}>

        <Button onClick={onClickPostModal} disabled={props.currentNodeId === ""}>
          <NoteAddOutlinedIcon />
        </Button>

        <Button onClick={onClickDelModal} disabled={props.currentNodeId === "" || props.currentNodeId === '/Folder'} sx={{ color: "red" }}>
          <DeleteOutlineOutlinedIcon />
        </Button>

      </Container>

      <Dialog onClose={closeModal} open={postModalOpen}>
        <DialogTitle>
          新しいコンテンツを作成
        </DialogTitle>

        <Container
          component="form"
          sx={{ '& > :not(style)': { m: 2, width: '25ch' } }}
          noValidate
          autoComplete="off"
        >
          <TextField
            id="outlined-basic"
            label="フォルダ名"
            variant="outlined"
            disabled
            value={`${currentNodeId}/`}
          />
          <TextField
            id="outlined-basic"
            label="新しいコンテンツ名"
            variant="outlined"
            value={newContentName}
            onChange={(e) => setNewContentName(e.target.value)}
          />
        </Container>

        {isInvalidId &&
          <Alert severity="error" sx={{ mx: 3 }}>
            空欄または既存のコンテンツ名と重複しています。
          </Alert>
        }

        <DialogActions>
          <Button autoFocus onClick={clickCreateNewContent}>OK</Button>
        </DialogActions>

      </Dialog>

      <Dialog onClose={closeModal} open={delModalOpen}>
        <DialogTitle>
          コンテンツを削除
        </DialogTitle>

        <DialogContent>
          そのコンテンツとすべての子コンテンツが削除されます。
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