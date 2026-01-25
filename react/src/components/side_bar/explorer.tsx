import ArticleOutlinedIcon from '@mui/icons-material/ArticleOutlined';
import FolderIcon from '@mui/icons-material/Folder';
import FolderOpenIcon from '@mui/icons-material/FolderOpen';
import { Box } from "@mui/material";
import { RichTreeView } from '@mui/x-tree-view/RichTreeView';
import { useState } from 'react';
import { useNavigate } from "react-router-dom";

import type { Tree } from '@/src/lib/types';

import TreeHandler from '@/src/lib/tree_handler';


function Explorer(props: { node_id: string, tree: Tree }) {
  const navigate = useNavigate();
  const [expandedItems, setExpandedItems] = useState<string[]>([]);

  const tree_handler = new TreeHandler(props.tree);
  const parents = tree_handler.getParentNodeIds(props.node_id);
  const displayedExpanded = [
    ...new Set([...expandedItems, ...parents, props.tree.id]),
  ];

  return (
    <>
      <Box >
        <RichTreeView
          sx={{ backgroundColor: "rgba(245, 245, 245)" }}
          items={[props.tree]}
          onItemClick={(_, id) => {
            navigate(`/main/${id}`);
          }}
          selectedItems={props.node_id}
          expandedItems={displayedExpanded}
          onExpandedItemsChange={(_, ids) => setExpandedItems(ids)}
          slots={{
            expandIcon: FolderIcon,
            collapseIcon: FolderOpenIcon,
            endIcon: ArticleOutlinedIcon,
          }}
        />
      </Box>
    </>
  );
};

export default Explorer;